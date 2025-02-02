# services/views.py
from rest_framework import generics, permissions
from .models import ServiceOrder
from .serializers import ServiceOrderSerializer

class ServiceOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceOrder.objects.filter(user=self.request.user)

class ServiceOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    permission_classes = [permissions.IsAuthenticated]