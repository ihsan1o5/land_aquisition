from property.models import Notification

def create_notification(title, detail, property, user, notification_type, meeting=None, comment=None):

    Notification.objects.create(
        title=title,
        detail=detail,
        property=property,
        user=user,
        comment=comment,
        notification_type=notification_type,
        meeting=meeting
    )


