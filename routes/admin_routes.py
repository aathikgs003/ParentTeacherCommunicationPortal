from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models import User, Student, Message, Announcement, Attendance, Report

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    return render_template('admin/dashboard.html')

@admin_bp.route('/manage_users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('admin.add_user'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('admin.add_user'))
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/add_user.html')

@admin_bp.route('/manage_students')
@login_required
def manage_students():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    students = Student.query.all()
    parents = User.query.filter_by(role='parent').all()
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('admin/manage_students.html', students=students, parents=parents, teachers=teachers)

@admin_bp.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        name = request.form.get('name')
        grade = request.form.get('grade')
        parent_id = request.form.get('parent_id')
        teacher_id = request.form.get('teacher_id')
        student = Student(name=name, grade=grade, parent_id=parent_id, teacher_id=teacher_id)
        db.session.add(student)
        db.session.commit()
        flash('Student added and teacher assigned successfully')
        return redirect(url_for('admin.manage_students'))
    parents = User.query.filter_by(role='parent').all()
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('admin/add_student.html', parents=parents, teachers=teachers)

@admin_bp.route('/assign_teacher/<int:student_id>', methods=['GET', 'POST'])
@login_required
def assign_teacher(student_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        student.teacher_id = teacher_id
        db.session.commit()
        flash('Teacher assigned successfully')
        return redirect(url_for('admin.manage_students'))
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('admin/assign_teacher.html', student=student, teachers=teachers)

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        user.is_active = 'is_active' in request.form
        db.session.commit()
        flash('User updated successfully')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot delete your own account')
        return redirect(url_for('admin.manage_users'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/view_logs')
@login_required
def view_logs():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    # Show recent messages, announcements, and attendance changes as logs
    messages = Message.query.order_by(Message.timestamp.desc()).limit(20).all()
    announcements = Announcement.query.order_by(Announcement.timestamp.desc()).limit(10).all()
    attendance = Attendance.query.order_by(Attendance.timestamp.desc()).limit(20).all()
    logs = []
    for msg in messages:
        logs.append({
            'type': 'Message',
            'description': f'{msg.sender.username} sent message to {msg.recipient.username}: {msg.subject}',
            'timestamp': msg.timestamp
        })
    for ann in announcements:
        logs.append({
            'type': 'Announcement',
            'description': f'{ann.teacher.username} posted announcement: {ann.title}',
            'timestamp': ann.timestamp
        })
    for att in attendance:
        logs.append({
            'type': 'Attendance',
            'description': f'Attendance marked for {att.student.name} by {att.teacher.username}: {att.status}',
            'timestamp': att.timestamp
        })
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    logs = logs[:50]  # Limit to 50 entries
    return render_template('admin/view_logs.html', logs=logs)
