from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from .serializers import StreamSerializer, UserProfileSerializer, \
    SynchSerializer, SynchMembershipSerializer, TextNoteSerializer, \
    NoteSerializer, ImageNoteSerializer
from .permissions import IsAdminOrReadOnly, IsSuperUserOrOwner, IsSuperUser
from .models import UserProfile, Synch, SynchMembership, Stream,\
      Note, TextNote, ImageNote

# Create your views here.

"""

"""
class UserProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self): 
        # only the user's profile
        return UserProfile.objects.select_related("user").all()
    
    def get_serializer_class(self):
        return UserProfileSerializer
    
    # to autofill the user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def me(self, request):
        user_profile = self.get_queryset().filter(user=request.user).first()
        if user_profile:
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

# end of UserProfileViewSet
    

"""

"""
class SynchViewSet (ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Synch.objects.select_related("creator").filter(members__member__user=user)
    
    def get_serializer_class(self):
        return SynchSerializer
    
    def perform_create(self, serializer):
        # get user making the request
        user = self.request.user
        # get the profile of this user
        profile = UserProfile.objects.get(user=user)

        with transaction.atomic():
            synch = serializer.save(creator=profile)
            SynchMembership.objects.create(synch=synch, member=profile)

# end of SynchViewSet


"""

"""
class SynchMembershipViewSet (ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SynchMembership.objects.filter(member__user=user)
    
    def get_serializer_class(self):
        return SynchMembershipSerializer

# end of SynchMembershipViewSet


"""

"""
class StreamViewSet (ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Stream.objects.filter(creator__user=user)
    
    def get_serializer_class(self):
        return StreamSerializer
    
    def perform_create(self, serializer):
        # get user making the request
        user = self.request.user
        # get the profile of this user
        profile = UserProfile.objects.get(user=user)

        with transaction.atomic():
            serializer.save(creator=profile)

# end of StreamViewSet


class NoteViewSet (ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Note.objects.filter(stream_id=self.kwargs['stream_pk'])
    
    def get_serializer_class(self):
        return NoteSerializer
    
    def perform_create(self, serializer):
        # get user making the request
        user = self.request.user
        # get the profile of this user
        profile = UserProfile.objects.get(user=user)

        with transaction.atomic():
            stream = Stream.objects.get(id=self.kwargs['stream_pk'])
            serializer.save(taker=profile, stream=stream)

# end of NoteViewSet

class TextNoteViewSet (ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return TextNote.objects.filter(note_id=self.kwargs['note_pk'])
    
    def get_serializer_class(self):
        return TextNoteSerializer
    
    def perform_create(self, serializer):
        with transaction.atomic():
            note = Note.objects.get(id=self.kwargs['note_pk'])
            serializer.save(note=note)
    
# end of TextNoteViewSet


class ImageNoteViewSet (ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return ImageNote.objects.filter(note_id=self.kwargs['note_pk'])
    
    def get_serializer_class(self):
        return ImageNoteSerializer
    
    def perform_create(self, serializer):
        with transaction.atomic():
            note = Note.objects.get(id=self.kwargs['note_pk'])
            serializer.save(note=note)
    
# end of ImageNoteViewSet
