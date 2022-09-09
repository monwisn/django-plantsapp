from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_mail_task():
    print("Mail sending...")
    subject = "Time for plants!"
    message = 'Friendly reminder:' \
              'Remember to water your plants today!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['monwisn3@gmail.com', 'bartkram11@gmail.com']
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return "Mail has been sent to users successfully."
