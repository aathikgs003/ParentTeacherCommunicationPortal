from app import create_app
from models import User, Student, db

def populate_db():
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if users already exist
        if User.query.first():
            print("Database already populated.")
            return

        # Create admin user
        admin = User(
            username='admin',
            email='admin@school.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')

        # Create teacher user
        teacher = User(
            username='teacher1',
            email='teacher@school.com',
            role='teacher',
            is_active=True
        )
        teacher.set_password('teacher123')

        # Create parent user
        parent = User(
            username='parent1',
            email='parent@school.com',
            role='parent',
            is_active=True
        )
        parent.set_password('parent123')

        # Add users to database
        db.session.add(admin)
        db.session.add(teacher)
        db.session.add(parent)
        db.session.commit()

        # Create a sample student
        student = Student(
            name='John Doe',
            grade='5th Grade',
            parent_id=parent.id,
            teacher_id=teacher.id
        )
        db.session.add(student)
        db.session.commit()

        print("Database populated with sample users:")
        print("Admin: username='admin', password='admin123'")
        print("Teacher: username='teacher1', password='teacher123'")
        print("Parent: username='parent1', password='parent123'")

if __name__ == '__main__':
    populate_db()
