from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_model import User
from .student_model import Student
from .message_model import Message
from .announcement_model import Announcement
from .attendance_model import Attendance
from .report_model import Report

__all__ = ['db', 'User', 'Student', 'Message', 'Announcement', 'Attendance', 'Report']
