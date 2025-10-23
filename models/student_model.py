from . import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    parent = db.relationship('User', foreign_keys=[parent_id], backref='children')
    teacher = db.relationship('User', foreign_keys=[teacher_id], backref='students')

    def __repr__(self):
        return f'<Student {self.name}>'
