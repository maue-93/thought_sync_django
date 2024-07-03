from django.urls import re_path
from harmony import consumers

websocket_urlpatterns = [
    re_path(r'ws/harmony/$', consumers.HomeConsumer.as_asgi()),
]


