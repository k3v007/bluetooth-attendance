from flask import url_for
from flask_mail import Message

from btattendance import mail
from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


def send_reset_mail(user):
    token = user.get_reset_token()
    print(token)
    print(url_for('users.reset_password', token=token, _external=True))
    msg = Message(subject='Password Reset Request!',
                  sender='noreply@btattendance.com',
                  recipients=[user.email],
                  body=f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you didn't make this request then simply ignore this email and changes will be made!
''')
    mail.send(msg)
