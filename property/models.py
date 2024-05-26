from django.db import models
from django.contrib.auth.models import User

class PropertyListing(models.Model):
    STATUS_CHOICES = (
        ('APPROVED', 'approved'),
        ('PENDING', 'pending'),
        ('UNDER DISCUSSION', 'under discussion'),
        ('REJECTED', 'REJECT'),
    )

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    property_type = models.CharField(max_length=100, blank=True, null=True)
    listing_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    address = models.CharField(max_length=255, null=True, blank=True, default="X-Y-Z")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class PropertyComment(models.Model):
    comment = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    property = models.ForeignKey(PropertyListing, on_delete=models.DO_NOTHING, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
    
class Meeting(models.Model):
    admin = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='admin_meetings')
    landowner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='landowner_meetings')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f"Meeting on {self.date} at {self.time} with {self.landowner}"
    
class Notification(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    detail = models.TextField(null=True, blank=True)
    property = models.ForeignKey(PropertyListing, on_delete=models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    comment = models.ForeignKey(PropertyComment, on_delete=models.DO_NOTHING, blank=True, null=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_readed = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

