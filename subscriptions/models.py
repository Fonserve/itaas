from django.db import models
from django.conf import settings

# Create your models here.
class SubscriptionTier(models.Model):
    TIER_CHOICES = (
        ('essential', 'Essential Support'),
        ('general', 'General Support'),
        ('enterprise', 'Enterprise Support'),
    )
    name = models.CharField(max_length=50, choices=TIER_CHOICES, unique=True)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    tier = models.ForeignKey(SubscriptionTier, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    next_billing_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.tier}"
