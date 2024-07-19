from django.urls import re_path
from harmony import consumers

websocket_urlpatterns = [
    # room_name below will be the id of an user's profile
    re_path(r'ws/home/(?P<room_name>[^/]+)/$', consumers.HomeUserConsumer.as_asgi()),

    # room_name below will be the id of a synch
    re_path(r'ws/synch/(?P<room_name>[^/]+)/$', consumers.SynchConsumer.as_asgi()),
    
    # room_name below will be the id of a stream
    re_path(r'ws/stream/(?P<room_name>[^/]+)/$', consumers.StreamConsumer.as_asgi()),
]


