from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.homeView, name='home'),
    path('update_property/<int:pk>/', views.updatePropertyView, name='update_property'),
    path('property_detail/<int:pk>/', views.propertyDetailView, name='property_detail'),
    path('delete_property/<int:pk>/', views.deletePropertyView, name='delete_property'),
    path('update_property_status/<int:pk>/', views.updatePropertyStatusView, name='update_property_status'),

    path('update_comment/<int:pk>/', views.updateComment, name='update_comment'),
    path('delete_comment/<int:comment_pk>/<int:property_pk>/', views.deleteCommentView, name='delete_comment'),
    path('fetch_notifications/', views.fetch_notifications, name='fetch_notifications'),
    path('mark_notification_read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('view_notification_detail/<int:notification_pk>/<int:property_pk>/', views.viewNotificationDetail, name='view_notification_detail'),

    path('confirm_meeting/<int:meeting_id>/', views.confirmMeeting, name='confirm_meeting'),
    path('details/<int:meeting_id>/', views.meetingDetails, name='meeting_details'),
    path('calendar/<int:property_pk>/', views.calendarView, name='calendar'),
    path('available_time_slots/', views.availableTimeSlots, name='available_time_slots'),
    path('book_meeting/', views.bookMeeting, name='book_meeting'),
    path('meetings/<int:user_pk>/', views.fetchAllMeetings, name='meetings'),
    path('attend_meeting/<int:meeting_id>/', views.attendMeeting, name='attend_meeting'),
]

