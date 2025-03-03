from django.db.models.signals import post_save
from django.dispatch import receiver
from billing.models import Invoice
from messaging.models import Message
from services.models import ServiceOrder
from .utils import create_billing_notification, create_message_notification, create_service_notification

@receiver(post_save, sender=Invoice)
def invoice_notification(sender, instance, created, **kwargs):
    if created:
        create_billing_notification(
            recipient=instance.user,
            invoice=instance
        )

@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    if created:
        create_message_notification(
            recipient=instance.recipient,
            message_obj=instance
        )

@receiver(post_save, sender=ServiceOrder)
def service_order_notification(sender, instance, created, **kwargs):
    if created:
        create_service_notification(
            recipient=instance.user,
            service_order=instance
        )