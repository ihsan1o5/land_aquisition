from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'meetings/(?P<meeting_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
