from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models import User, Message, Announcement, Report, Attendance, Student

parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    return render_template('parent/dashboard.html')

@parent_bp.route('/view_announcements')
@login_required
def view_announcements():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    # Get announcements from teachers assigned to the parent's children
    announcements = Announcement.query.join(User, Announcement.teacher_id == User.id).join(Student, Student.teacher_id == User.id).filter(Student.parent_id == current_user.id).distinct().all()
    return render_template('parent/view_announcements.html', announcements=announcements)

@parent_bp.route('/send_feedback', methods=['GET', 'POST'])
@login_required
def send_feedback():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        subject = request.form.get('subject')
        content = request.form.get('content')
        message = Message(sender_id=current_user.id, recipient_id=teacher_id, subject=subject, content=content)
        db.session.add(message)
        db.session.commit()
        flash('Feedback sent successfully')
        return redirect(url_for('parent.send_feedback'))
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('parent/send_feedback.html', teachers=teachers)

@parent_bp.route('/view_reports')
@login_required
def view_reports():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    reports = Report.query.join(Student).filter(Student.parent_id == current_user.id).all()
    return render_template('parent/view_reports.html', reports=reports)

@parent_bp.route('/attendance_log')
@login_required
def attendance_log():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    attendance_records = Attendance.query.join(Student).filter(Student.parent_id == current_user.id).all()
    return render_template('parent/attendance_log.html', attendance_records=attendance_records)

@parent_bp.route('/view_messages')
@login_required
def view_messages():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('parent/view_messages.html', messages=messages)

@parent_bp.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        subject = request.form.get('subject')
        content = request.form.get('content')
        message = Message(sender_id=current_user.id, recipient_id=recipient_id, subject=subject, content=content)
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully')
        return redirect(url_for('parent.send_message'))
    # Parents can send messages to teachers of their children
    teachers = User.query.filter_by(role='teacher').join(Student, Student.teacher_id == User.id).filter(Student.parent_id == current_user.id).distinct().all()
    return render_template('parent/send_message.html', teachers=teachers)

@parent_bp.route('/profile')
@login_required
def profile():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    children = Student.query.filter_by(parent_id=current_user.id).all()
    return render_template('parent/profile.html', children=children)

@parent_bp.route('/contact_teacher/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def contact_teacher(teacher_id):
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    teacher = User.query.get_or_404(teacher_id)
    # Check if teacher is assigned to parent's child
    has_access = Student.query.filter_by(parent_id=current_user.id, teacher_id=teacher_id).first() is not None
    if not has_access:
        flash('You can only contact teachers assigned to your children')
        return redirect(url_for('parent.dashboard'))
    if request.method == 'POST':
        subject = request.form.get('subject')
        content = request.form.get('content')
        message = Message(sender_id=current_user.id, recipient_id=teacher_id, subject=subject, content=content)
        db.session.add(message)
        db.session.commit()
        flash('Message sent to teacher successfully')
        return redirect(url_for('parent.contact_teacher', teacher_id=teacher_id))
    return render_template('parent/contact_teacher.html', teacher=teacher)

@parent_bp.route('/contact_teacher_list')
@login_required
def contact_teacher_list():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    # Get teachers assigned to parent's children
    teachers = User.query.filter_by(role='teacher').join(Student, Student.teacher_id == User.id).filter(Student.parent_id == current_user.id).distinct().all()
    return render_template('parent/contact_teacher_list.html', teachers=teachers)
