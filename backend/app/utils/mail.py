from flask_mail import Message
from app import mail


def send_email(subject, recipients, body, sender="noreply@quizmaster.com"):
    msg = Message(subject=subject, recipients=recipients, body=body, sender=sender)
    mail.send(msg)
