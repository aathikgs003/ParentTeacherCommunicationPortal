from . import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', backref='reports')
    teacher = db.relationship('User', backref='uploaded_reports')

    def __repr__(self):
        return f'<Report {self.title}>'
