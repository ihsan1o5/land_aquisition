from django.contrib import admin
from .models import PropertyListing, PropertyComment, Notification, Meeting

admin.site.register(PropertyListing)
admin.site.register(PropertyComment)
admin.site.register(Notification)
admin.site.register(Meeting)

