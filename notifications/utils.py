from .models import Notification

def create_notification(recipient, notification_type, title, message, content_object=None):
    """
    Create a new notification
    
    Args:
        recipient: User receiving the notification
        notification_type: Type of notification (from NOTIFICATION_TYPES)
        title: Notification title
        message: Notification message
        content_object: Optional related object (invoice, message, etc.)
    """
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        content_object=content_object
    )
    return notification

def create_billing_notification(recipient, invoice, message=None):
    """Helper to create billing notifications"""
    title = f"Invoice #{invoice.invoice_number} - ${invoice.amount}"
    message = message or f"A new invoice for ${invoice.amount} is due on {invoice.due_date}"
    return create_notification(
        recipient=recipient,
        notification_type='billing',
        title=title,
        message=message,
        content_object=invoice
    )

def create_message_notification(recipient, message_obj):
    """Helper to create message notifications"""
    sender_name = message_obj.sender.get_full_name() or message_obj.sender.username
    title = f"New message from {sender_name}"
    message = message_obj.content[:100] + "..." if len(message_obj.content) > 100 else message_obj.content
    return create_notification(
        recipient=recipient,
        notification_type='message',
        title=title,
        message=message,
        content_object=message_obj
    )

def create_service_notification(recipient, service_order, message=None):
    """Helper to create service order notifications"""
    title = f"Update for {service_order.service.name}"
    message = message or f"Service order status updated to: {service_order.get_status_display()}"
    return create_notification(
        recipient=recipient,
        notification_type='service',
        title=title,
        message=message,
        content_object=service_order
    )
