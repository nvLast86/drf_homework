from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task()
def change_status_user():
    users = User.objects.all().filter(is_active=True)
    for user in users:
        if user.last_login:
            if timezone.now() - user.last_login > timedelta(days=31):
                user.is_active = False
                user.save()
