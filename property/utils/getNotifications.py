from property.models import Notification, PropertyListing

def get_notifications_for_user(user, property_filter=None, notification_types=None):
    if property_filter is None:
        property_filter = PropertyListing.objects.filter(owner=user, is_active=True)
    
    if notification_types is None:
        notification_types = ['comment', 'status']

    notifications = Notification.objects.filter(
        property__in=property_filter,
        is_readed=False,
        notification_type__in=notification_types
    ).exclude(user=user)
    
    return notifications