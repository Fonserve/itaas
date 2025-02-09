from django.contrib import admin
from .models import SubscriptionTier, Subscription

# Register your models here.
admin.site.register(SubscriptionTier)
admin.site.register(Subscription)