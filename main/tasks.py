from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from main.models import NewsletterUser
from plants_app import celery_app


# We use the shared_task decorator to define tasks that can be shared across multiple Django apps.
# It allows these tasks to be used in any application.
@shared_task
def send_mail_task():
    print("Mail sending...")
    subject = "Time for plants!"
    message = 'Friendly reminder:' \
              'Remember to water your plants today!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['lewalski12@gmail.com', "bartkram11@gmail.com"]
    # send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)
    print("Mail has been sent to users successfully.")
    return send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)



@celery_app.task(bind=True)
def send_reminder_3_days():
    print("Mail sending...")
    subject = "Time for plants!"
    message = """Friendly reminder:

    Remember to water your plants today!
    Don't let them die :(


    Sincerely,
        The Watering Plants Application Team"""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['email@gmail.com', "email@gmail.com"]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return "Mail has been sent to users successfully."


@celery_app.task
def send_reminder_7_days():
    print("Mail sending...")
    subject = "Time for a weekly plants inspection!"
    message = """Friendly reminder:

    A week has passed, it's time to take care of the plants.
    Remember to water them today!


    Sincerely,
        The Watering Plants Application Team"""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['email@gmail.com', "email@gmail.com"]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return "Mail has been sent to users successfully."


@shared_task()
def send_reminder_14_days():
    print("Mail sending...")
    subject = "We are waiting for you! ~ your plants"
    message = """Two weeks flew by like one day.

    Maybe you have already forgotten about them, so we would like to remind you:
    It's time to water your plants!

    They also deserve a little attention from time to time.

    Sincerely,
        The Watering Plants Application Team"""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['email@gmail.com', "email@gmail.com"]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return "Mail has been sent to users successfully."


@shared_task()
def send_weekly_newsletters():
    newsletter_users = NewsletterUser.objects.all()
    subject = 'Weekly Newsletter'
    message = '''
    Hello,

    This is your weekly newsletter with our tips to keep plants healthy and beautiful.
    We hope our advice is useful.

    If you have any suggestions for our newsletter, please let us know at:

    plantsapp@contact.com


    Best Regards,
    PlantsApp Team.
    '''
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email for user in newsletter_users]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    return 'Weekly newsletter has been sent'


@shared_task
def send_notification(subject, message, from_email, recipient_list):
    print('start')
    subject = "Time for plants!"
    message = """Friendly reminder:

        Remember to water your plants today!
        Don't let them die :(


        Sincerely,
            The Watering Plants Application Team"""
    from_email = 'bartkram11@gmail.com'
    recipient_list = ['lewalski12@gmail.com', "bartkram11@gmail.com"]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)
    print('end')
