# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.models import ServiceOrder, Service
from subscriptions.models import Subscription
from billing.models import Invoice
from django.utils import timezone
from django.views.generic import TemplateView

@login_required
def DashboardView(request):
    # Get the latest 5 unread notifications
    from notifications.models import Notification
    
    context = {
        'subscriptions': Subscription.objects.filter(user=request.user),
        'invoices': request.user.invoices.all(),
        'service_orders': request.user.service_orders.all(),
        'services': Service.objects.all(),
        'recent_notifications': Notification.objects.filter(
            recipient=request.user,
            read=False
        ).order_by('-created_at')[:5],
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

@login_required
def MessagingView(request):
    # Get all unique users the current user has communicated with
    from messaging.models import Message
    from django.db.models import Q, Count, Max
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Find users who have conversations with the current user
    user_conversations = User.objects.filter(
        Q(sent_messages__recipient=request.user) | Q(received_messages__sender=request.user)
    ).distinct().exclude(id=request.user.id)
    
    contacts = []
    for user in user_conversations:
        # Count unread messages from this user
        unread_count = Message.objects.filter(
            sender=user, 
            recipient=request.user,
            read=False
        ).count()
        
        # Get the last message between these users
        last_message = Message.objects.filter(
            Q(sender=user, recipient=request.user) | Q(sender=request.user, recipient=user)
        ).order_by('-timestamp').first()
        
        contacts.append({
            'id': user.id,
            'name': user.get_full_name() or user.username,
            'unread': unread_count,
            'last_message': last_message.content if last_message else ""
        })
    
    # Add support team as a default contact if no existing contacts
    if not contacts:
        # Find a staff user for support
        support_user = User.objects.filter(is_staff=True).first()
        if support_user:
            contacts.append({
                'id': support_user.id,
                'name': 'Support Team',
                'unread': 0,
                'last_message': "How can we help you today?"
            })
    
    # Get a list of available users for new chats
    # This will be used for initial rendering, but the full list will be loaded via AJAX
    available_users = User.objects.exclude(id=request.user.id).order_by('username')[:10]
    
    context = {
        'contacts': contacts,
        'available_users': available_users,
    }
    
    return render(request, 'dashboard/messaging.html', context)