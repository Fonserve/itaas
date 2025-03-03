from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'title', 'read', 'created_at')
    list_filter = ('notification_type', 'read', 'created_at')
    search_fields = ('title', 'message', 'recipient__username', 'recipient__email')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        # Filter by recipient for non-superusers
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(recipient=request.user)
