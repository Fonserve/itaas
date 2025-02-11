from django.db import models
from django.conf import settings

class SubscriptionPlan(models.Model):
    TIER_CHOICES = [
        ('essential', 'Essential'),
        ('general', 'General'),
        ('enterprise', 'Enterprise'),
    ]
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    features = models.JSONField(default=dict)  # Detailed SLAs and features
    base_monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    base_annual_rate = models.DecimalField(max_digits=10, decimal_places=2)
    min_contract_months = models.PositiveIntegerField(default=12)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    CONTRACT_TERMS = [
        ('yearly', 'Yearly'),
        ('two_year', 'Two Years'),
        ('three_year', 'Three Years'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscriptions')
    contract_term = models.CharField(max_length=20, choices=CONTRACT_TERMS)
    start_date = models.DateField()
    end_date = models.DateField()
    billing_day = models.PositiveSmallIntegerField(help_text="Day of the month billing is processed")
    next_billing_date = models.DateField()
    actual_monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    auto_renew = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
