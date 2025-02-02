from rest_framework import serializers
from .models import Subscription, SubscriptionTier

class SubscriptionTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionTier
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    tier = SubscriptionTierSerializer()

    class Meta:
        model = Subscription
        fields = '__all__'