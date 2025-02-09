# services/models.py
from django.db import models
from django.conf import settings

class Service(models.Model):
    BILLING_FREQUENCY = [
        ('one_time', 'One-Time Payment'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_frequency = models.CharField(max_length=20, choices=BILLING_FREQUENCY)
    estimated_duration = models.PositiveIntegerField(help_text="Duration in days")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ServiceOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_billed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.service.name} for {self.user.username}"