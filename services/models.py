# services/models.py
from django.db import models
from django.conf import settings

class ServiceOrder(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('onetime', 'One-Time Service'),
        ('recurring', 'Recurring Service'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_orders')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    description = models.TextField()
    scheduled_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.service_type}"