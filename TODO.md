# TODO: Create Parent-Teacher Communication Portal Flask Project

## Step 1: Create Directories [COMPLETED]
- Create static/, static/css/, static/js/, static/uploads/, static/uploads/reports/, static/uploads/profile_pics/
- Create templates/, templates/teacher/, templates/parent/, templates/admin/
- Create instance/
- Create models/
- Create routes/
- Create utils/

## Step 2: Create Root Files [COMPLETED]
- app.py: Main Flask application
- config.py: Configuration settings
- requirements.txt: Python dependencies
- attendance.db: SQLite database (if needed, or skip as auto-created)

## Step 3: Create Models [COMPLETED]
- models/__init__.py
- models/user_model.py
- models/student_model.py
- models/message_model.py
- models/announcement_model.py
- models/attendance_model.py
- models/report_model.py

## Step 4: Create Routes [COMPLETED]
- routes/__init__.py
- routes/main_routes.py
- routes/auth_routes.py
- routes/teacher_routes.py
- routes/parent_routes.py
- routes/admin_routes.py

## Step 5: Create Templates [COMPLETED]
- templates/base.html
- templates/index.html
- templates/login.html
- templates/register.html
- templates/teacher/dashboard.html
- templates/teacher/announcements.html
- templates/teacher/send_message.html
- templates/teacher/view_parent_messages.html
- templates/teacher/upload_report.html
- templates/teacher/attendance.html
- templates/parent/dashboard.html
- templates/parent/view_announcements.html
- templates/parent/send_feedback.html
- templates/parent/view_reports.html
- templates/parent/attendance_log.html
- templates/admin/dashboard.html
- templates/admin/manage_users.html
- templates/admin/view_logs.html

## Step 6: Create Static Files [COMPLETED]
- static/css/style.css
- static/css/dashboard.css
- static/js/main.js
- static/js/validation.js

## Step 7: Create Utils [COMPLETED]
- utils/__init__.py
- utils/database.py
- utils/email_service.py
- utils/decorators.py
- utils/helpers.py

## Step 8: Followup [COMPLETED]
- Install dependencies: pip install -r requirements.txt
- Initialize database if needed
- Run the app: python app.py
