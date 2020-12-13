from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

import institution.models as my_models


@shared_task
def send_email(institution_id, vacancy_id, created):
    import time
    time.sleep(5)
    if created:
        institution = my_models.Institution.objects.get(pk=institution_id)
        vacancy = my_models.Vacancy.objects.get(pk=vacancy_id)
        print(vacancy)
        if institution.subscribers:
            for subscriber in institution.subscribers.all():
                send_mail(
                    'New vacancies!!!',
                    vacancy.vacancy,
                    settings.EMAIL_HOST_USER,
                    [str(subscriber.email)],
                    fail_silently=False,
                )
    else:
        pass