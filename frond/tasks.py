# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Subscription
from datetime import timedelta

@receiver(post_save, sender=User)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        expiry_date = timezone.now() + timedelta(days=30)  # Set expiry date to 1 month from registration
        Subscription.objects.create(user=instance, expiry_date=expiry_date)

# tasks.py
from celery import shared_task
from .models import Subscription
from django.utils import timezone
from datetime import timedelta
from twilio.rest import Client
from django.conf import settings

@shared_task
def check_subscription_expiry():
    tomorrow = timezone.now() + timedelta(days=1)
    subscriptions = Subscription.objects.filter(expiry_date=tomorrow)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for subscription in subscriptions:
        message = client.messages.create(
            body=f'Your subscription is expiring tomorrow.',
            from_=settings.TWILIO_NUMBER,
            to=subscription.user.phone_number
        )
