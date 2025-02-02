from rest_framework import generics, permissions
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class SubscriptionCreateView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]