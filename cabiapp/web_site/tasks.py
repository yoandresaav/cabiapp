from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail


logger = get_task_logger(__name__)


@task(name="send_feedback_email_task")
def send_feedback_email_task(email, message):
    """sends an email when feedback form is filled successfully"""
    print("Haciendo de las mias")
    logger.info("Sent feedback email aaaaaaaaaaa")
    return send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )