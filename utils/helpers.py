import os
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime, timedelta

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, subfolder=''):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    return None

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def format_datetime(dt):
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return ''

def format_date(dt):
    if dt:
        return dt.strftime('%Y-%m-%d')
    return ''

def get_time_ago(dt):
    if not dt:
        return ''
    now = datetime.utcnow()
    diff = now - dt

    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600} hours ago"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return "Just now"

def paginate_query(query, page, per_page=10):
    return query.paginate(page=page, per_page=per_page, error_out=False)

def generate_unique_filename(original_filename):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(original_filename)
    return f"{name}_{timestamp}{ext}"

def validate_date_string(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_week_dates(date):
    """Get all dates for the week containing the given date"""
    start_of_week = date - timedelta(days=date.weekday())
    return [start_of_week + timedelta(days=i) for i in range(7)]

def calculate_attendance_percentage(attendance_records):
    if not attendance_records:
        return 0
    present_count = sum(1 for record in attendance_records if record.status == 'present')
    return round((present_count / len(attendance_records)) * 100, 2)

def get_user_initials(name):
    """Get initials from a full name"""
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    elif parts:
        return parts[0][:2].upper()
    return "U"

def truncate_text(text, max_length=100):
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def is_valid_role(role):
    return role in ['teacher', 'parent', 'admin']

def get_role_display_name(role):
    role_names = {
        'teacher': 'Teacher',
        'parent': 'Parent',
        'admin': 'Administrator'
    }
    return role_names.get(role, role.title())

def get_status_color(status):
    colors = {
        'present': '#28a745',
        'absent': '#dc3545',
        'late': '#ffc107'
    }
    return colors.get(status.lower(), '#6c757d')
