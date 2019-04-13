from flask import current_app
from flask_mail import Message

from app import mail


def send_reset_mail(email, url):
    app = current_app._get_current_object()
    msg = Message(subject='Password Reset Request!',
                  sender=app.config['FLASY_MAIL_SENDER'],
                  recipients=[email],
                  body=f'''To reset your password, visit the following link:
{url}

If you didn't make this request then simply ignore this email and changes will be made!
''')
    mail.send(msg)
