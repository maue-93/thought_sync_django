from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('user_profiles', views.UserProfileViewSet, basename='user_profiles')
router.register('synchs', views.SynchViewSet, basename='synchs')
router.register('synch_memberships', views.SynchMembershipViewSet, basename='synch_memberships')
router.register('streams', views.StreamViewSet, basename='streams')

# register notes endpoints under stream instance endpoint
# When lookup='stream', it means that the URL parameter for the Stream instance will be named stream_pk (by default) in the Note viewset
streams_router = NestedDefaultRouter(router, r'streams', lookup='stream') 
streams_router.register(r'notes', views.NoteViewSet, basename='notes')
# register text and image notes under note instance endpoint
notes_router = NestedDefaultRouter(streams_router, r'notes', lookup='note')
notes_router.register(r'texts', views.TextNoteViewSet, basename='texts')
notes_router.register(r'images', views.ImageNoteViewSet, basename='images')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(streams_router.urls)),
    path(r'', include(notes_router.urls)),
]