from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import os

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def reset_db():
    with current_app.app_context():
        db.drop_all()
        db.create_all()

def backup_db():
    # Simple backup function - in production, use proper backup solutions
    import shutil
    from datetime import datetime

    db_path = current_app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if os.path.exists(db_path):
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(db_path, os.path.join('backups', backup_name))
        return backup_name
    return None

def get_db_stats():
    """Get database statistics"""
    with current_app.app_context():
        from models import User, Student, Message, Announcement, Attendance, Report

        stats = {
            'users': User.query.count(),
            'students': Student.query.count(),
            'messages': Message.query.count(),
            'announcements': Announcement.query.count(),
            'attendance_records': Attendance.query.count(),
            'reports': Report.query.count()
        }
        return stats
