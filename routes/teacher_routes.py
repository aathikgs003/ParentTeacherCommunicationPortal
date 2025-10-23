from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models import User, Message, Announcement, Attendance, Report, Student
from datetime import datetime

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    return render_template('teacher/dashboard.html')

@teacher_bp.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        announcement = Announcement(title=title, content=content, teacher_id=current_user.id)
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement posted successfully')
        return redirect(url_for('teacher.announcements'))
    announcements = Announcement.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/announcements.html', announcements=announcements)

@teacher_bp.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        subject = request.form.get('subject')
        content = request.form.get('content')
        message = Message(sender_id=current_user.id, recipient_id=recipient_id, subject=subject, content=content)
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully')
        return redirect(url_for('teacher.send_message'))
    parents = User.query.filter_by(role='parent').all()
    return render_template('teacher/send_message.html', parents=parents)

@teacher_bp.route('/view_parent_messages')
@login_required
def view_parent_messages():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    messages = Message.query.filter_by(recipient_id=current_user.id).all()
    return render_template('teacher/view_parent_messages.html', messages=messages)

@teacher_bp.route('/upload_report', methods=['GET', 'POST'])
@login_required
def upload_report():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        student_id = request.form.get('student_id')
        report = Report(title=title, content=content, student_id=student_id, teacher_id=current_user.id)
        db.session.add(report)
        db.session.commit()
        flash('Report uploaded successfully')
        return redirect(url_for('teacher.upload_report'))
    students = Student.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/upload_report.html', students=students)

@teacher_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        date_str = request.form.get('date')
        status = request.form.get('status')
        # Convert date string to date object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        attendance = Attendance(student_id=student_id, date=date, status=status, teacher_id=current_user.id)
        db.session.add(attendance)
        db.session.commit()
        flash('Attendance marked successfully')
        return redirect(url_for('teacher.attendance'))
    students = Student.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/attendance.html', students=students)

@teacher_bp.route('/view_students')
@login_required
def view_students():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    students = Student.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/view_students.html', students=students)

@teacher_bp.route('/view_reports')
@login_required
def view_reports():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    reports = Report.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/view_reports.html', reports=reports)

@teacher_bp.route('/view_messages')
@login_required
def view_messages():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('teacher/view_messages.html', messages=messages)

@teacher_bp.route('/send_message_to_parent/<int:parent_id>', methods=['GET', 'POST'])
@login_required
def send_message_to_parent(parent_id):
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    parent = User.query.get_or_404(parent_id)
    # Check if teacher has students with this parent
    has_access = Student.query.filter_by(teacher_id=current_user.id, parent_id=parent_id).first() is not None
    if not has_access:
        flash('You can only message parents of your students')
        return redirect(url_for('teacher.dashboard'))
    if request.method == 'POST':
        subject = request.form.get('subject')
        content = request.form.get('content')
        message = Message(sender_id=current_user.id, recipient_id=parent_id, subject=subject, content=content)
        db.session.add(message)
        db.session.commit()
        flash('Message sent to parent successfully')
        return redirect(url_for('teacher.send_message_to_parent', parent_id=parent_id))
    return render_template('teacher/send_message_to_parent.html', parent=parent)

@teacher_bp.route('/contact_parents')
@login_required
def contact_parents():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    # Get parents of teacher's students
    parents = User.query.filter_by(role='parent').join(Student, Student.parent_id == User.id).filter(Student.teacher_id == current_user.id).distinct().all()
    return render_template('teacher/contact_parents.html', parents=parents)

@teacher_bp.route('/profile')
@login_required
def profile():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    students = Student.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/profile.html', students=students)

@teacher_bp.route('/attendance_report')
@login_required
def attendance_report():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    attendance_records = Attendance.query.filter_by(teacher_id=current_user.id).order_by(Attendance.date.desc()).all()
    return render_template('teacher/attendance_report.html', attendance_records=attendance_records)
