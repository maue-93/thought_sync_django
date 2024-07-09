from django.db import transaction
from django.db.models import Q, Count
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from .serializers import StreamSerializer, UserProfileSerializer, \
    SynchSerializer, SynchMembershipSerializer, TextNoteSerializer, \
    NoteSerializer, ImageNoteSerializer, ImageNoteBulkSerializer
from .permissions import IsAdminOrReadOnly, IsSuperUserOrOwner, IsSuperUser
from .models import UserProfile, Synch, SynchMembership, Stream,\
    StreamMembership, Note, TextNote, ImageNote

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
        return SynchMembership.objects.filter(synch_id=self.kwargs['synch_pk'])
    
    def get_serializer_class(self):
        return SynchMembershipSerializer
    
    # remember that the serializer create function is also overriden
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(synch_id=self.kwargs['synch_pk'])

# end of SynchMembershipViewSet

"""

"""
class StreamViewSet (ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # get streams that are for everyone and the ones that the user is part of
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        filter_condition = Q(synch_id=self.kwargs['synch_pk']) & (Q(membership_type=Stream.EVERYONE) | Q(members__member=profile))
        queryset = Stream.objects.filter(filter_condition)
        # for any for everyone stream this user does not have membership to, create the membership
        streams = queryset.filter(~Q(members__member__user=user))
        for stream in streams:
            StreamMembership.objects.create(stream=stream, member=profile)
        return queryset
    
    def get_serializer_class(self):
        return StreamSerializer
    
    def perform_create(self, serializer):
        # get user making the request
        user = self.request.user
        # get the profile of this user
        profile = UserProfile.objects.get(user=user)

        with transaction.atomic():
            serializer.save(creator=profile, synch_id=self.kwargs['synch_pk'])

    # get the list of all the notes in this stream
    @action(detail=True, methods=['get'], url_path='content', url_name='content')
    def content(self, request, pk=None, synch_pk=None):
        # get all the text notes that are in this stream
        texts = TextNote.objects.filter(note__stream__id=pk)
        # serialize all the text notes
        texts_serializer = TextNoteSerializer(texts, many=True)
        # get all the notes that has images in it
        notes = Note.objects.annotate(image_count=Count('images')).filter(stream__id=pk, image_count__gt=0)
        # serialize the images in bulk of their respective notes
        image_bulks_serializer = ImageNoteBulkSerializer(notes, many=True)
        # now put the text and the image bulks in one list
        stream_content = texts_serializer.data + image_bulks_serializer.data
        return Response(stream_content)

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
        return ImageNote.objects.filter(note_id=self.kwargs['note_pk'])
    
    def get_serializer_class(self):
        return ImageNoteSerializer
    
    def perform_create(self, serializer):
        with transaction.atomic():
            note = Note.objects.get(id=self.kwargs['note_pk'])
            serializer.save(note=note)
    
# end of ImageNoteViewSet
