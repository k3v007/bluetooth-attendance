from flask_mail import Message

from app import mail, rq


@rq.job
def send_reset_mail(email, url):
    msg = Message(subject='Password Reset Request!',
                  sender='noreply@bluetooth_attendance.com',
                  recipients=[email],
                  body=f'''To reset your password, visit the following link:
{url}

If you didn't make this request then simply ignore this email and changes will be made!
''')
    mail.send(msg)
