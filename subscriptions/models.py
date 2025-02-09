from django.db import models
from django.conf import settings

class SubscriptionTier(models.Model):
    TIER_CHOICES = [
        ('essential', 'Essential Support'),
        ('general', 'General Support'),
        ('enterprise', 'Enterprise Support'),
    ]
    
    name = models.CharField(max_length=50, choices=TIER_CHOICES, unique=True)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    features = models.JSONField(default=dict)
    min_contract_months = models.PositiveIntegerField(default=12)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()

class Subscription(models.Model):
    CONTRACT_TERMS = [
        ('yearly', 'Yearly'),
        ('two_year', 'Two Years'),
        ('three_year', 'Three Years'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    tier = models.ForeignKey(SubscriptionTier, on_delete=models.PROTECT)
    contract_term = models.CharField(max_length=20, choices=CONTRACT_TERMS)
    start_date = models.DateField()
    end_date = models.DateField()
    next_billing_date = models.DateField()
    annual_rate = models.DecimalField(max_digits=10, decimal_places=2)
    auto_renew = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tier.get_name_display()}"
