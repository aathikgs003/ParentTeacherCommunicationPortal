from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def teacher_required(f):
    return role_required('teacher')(f)

def parent_required(f):
    return role_required('parent')(f)

def admin_required(f):
    return role_required('admin')(f)

def teacher_or_admin_required(f):
    return role_required('teacher', 'admin')(f)

def parent_or_admin_required(f):
    return role_required('parent', 'admin')(f)
