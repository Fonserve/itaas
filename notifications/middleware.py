from django.utils.deprecation import MiddlewareMixin

class NotificationMiddleware(MiddlewareMixin):
    """
    Middleware to add unread notification count to request context
    """
    
    def process_request(self, request):
        if request.user.is_authenticated:
            # Avoid unnecessary imports for unauthenticated users
            from .models import Notification
            request.unread_notifications_count = Notification.objects.filter(
                recipient=request.user, 
                read=False
            ).count()
        return None
