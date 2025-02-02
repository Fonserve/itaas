# services/serializers.py
from rest_framework import serializers
from .models import ServiceOrder

class ServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = '__all__'