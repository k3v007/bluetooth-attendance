import time

from bluetooth import discover_devices
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


@rq.job
def discover_bd(seconds=10):
    t_end = time.time() + seconds
    devices = set()

    while time.time() < t_end:
        temp = discover_devices()
        devices.update(temp)
    print(devices)
    return devices
