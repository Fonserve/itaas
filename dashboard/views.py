# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.models import Service
from subscriptions.models import Subscription
from django.utils import timezone

@login_required
def DashboardView(request):
    context = {
        'subscriptions': Subscription.objects.filter(user=request.user),
        'invoices': request.user.invoices.all(),
        'service_orders': request.user.service_orders.all(),
        'services': Service.objects.all(),
    }
    return render(request, 'dashboard/dashboard_home.html', context)

@login_required
def ServicesView(request):
    available_services = Service.objects.all()
    service_orders = request.user.service_orders.all()
    subscriptions = request.user.subscriptions.all()
    upcoming_orders = request.user.service_orders.filter(start_date__gt=timezone.now()).order_by('start_date')
    context = {
        'services': available_services,
        'service_orders': service_orders,
        'subscriptions': subscriptions,
        'upcoming_orders': upcoming_orders,
    }
    return render(request, 'dashboard/services.html', context)