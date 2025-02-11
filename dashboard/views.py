# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.models import ServiceOrder, Service
from subscriptions.models import Subscription
from billing.models import Invoice
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

@login_required
def MyServicesView(request):
    now = timezone.now().date()
    active_services = request.user.service_orders.filter(end_date__gte=now)
    past_services = request.user.service_orders.filter(end_date__lt=now)
    context = {
        'active_services': active_services,
        'past_services': past_services,
    }
    return render(request, 'dashboard/my_services.html', context)

@login_required
def SubscriptionsView(request):
    subscriptions = request.user.subscriptions.all()
    context = {'subscriptions': subscriptions}
    return render(request, 'dashboard/subscriptions.html', context)

@login_required
def PastServicesView(request):
    now = timezone.now().date()
    past_services = request.user.service_orders.filter(end_date__lt=now)
    context = {'past_services': past_services}
    return render(request, 'dashboard/past_services.html', context)

@login_required
def OrderingView(request):
    # For simplicity, we'll list available new orders:
    new_services = Service.objects.filter(is_active=True)
    available_subscriptions = Subscription.objects.filter(is_active=True)
    context = {
        'new_services': new_services,
        'available_subscriptions': available_subscriptions,
        # room for additional ordering categories
    }
    return render(request, 'dashboard/ordering.html', context)

@login_required
def AnalyticsView(request):
    # Placeholder: You can add analytics calculations here.
    context = {}
    return render(request, 'dashboard/analytics.html', context)

@login_required
def SettingsView(request):
    # Placeholder view for settings; functionality to be added later.
    context = {}
    return render(request, 'dashboard/settings.html', context)