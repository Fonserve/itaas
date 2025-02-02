# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def DashboardView(request):
    context = {
        'subscriptions': request.user.subscriptions.all(),
        'invoices': request.user.invoices.all(),
        'service_orders': request.user.service_orders.all(),
    }
    return render(request, 'dashboard/dashboard_home.html', context)