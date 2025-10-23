from flask_mail import Mail, Message
from flask import current_app, render_template
from threading import Thread

mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body, text_body=None):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    if text_body:
        msg.body = text_body

    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_welcome_email(user):
    subject = "Welcome to Parent-Teacher Communication Portal"
    recipients = [user.email]

    html_body = render_template('email/welcome.html', user=user)
    text_body = f"Welcome {user.username}! Your account has been created successfully."

    send_email(subject, recipients, html_body, text_body)

def send_message_notification(recipient, sender, message):
    subject = f"New Message from {sender.username}"
    recipients = [recipient.email]

    html_body = render_template('email/new_message.html',
                               recipient=recipient,
                               sender=sender,
                               message=message)
    text_body = f"You have a new message from {sender.username}: {message.subject}"

    send_email(subject, recipients, html_body, text_body)

def send_announcement_notification(recipient, announcement):
    subject = f"New Announcement: {announcement.title}"
    recipients = [recipient.email]

    html_body = render_template('email/new_announcement.html',
                               recipient=recipient,
                               announcement=announcement)
    text_body = f"New announcement: {announcement.title}"

    send_email(subject, recipients, html_body, text_body)

def send_report_notification(parent, report):
    subject = f"New Report for {report.student.name}"
    recipients = [parent.email]

    html_body = render_template('email/new_report.html',
                               parent=parent,
                               report=report)
    text_body = f"A new report has been uploaded for {report.student.name}: {report.title}"

    send_email(subject, recipients, html_body, text_body)

def send_password_reset_email(user, reset_token):
    subject = "Password Reset Request"
    recipients = [user.email]

    html_body = render_template('email/reset_password.html',
                               user=user,
                               reset_token=reset_token)
    text_body = f"Click the link to reset your password: {current_app.config['FRONTEND_URL']}/reset/{reset_token}"

    send_email(subject, recipients, html_body, text_body)
