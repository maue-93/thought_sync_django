from django.db import transaction
from django.db.models import Q, Count
from rest_framework import serializers, mixins, permissions

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework import status

from .serializers import UserProfileSerializer, SynchSerializer, \
    SynchMembershipSerializer, StreamSerializer, \
    StreamMembershipSerializer, TextNoteSerializer,NoteSerializer, \
    ImageNoteSerializer, ImageNoteBulkSerializer
from .permissions import IsCreatorOrReadOnly, IsMemberOrReadOnly, IsNoteTakerOrReadOnly
from .models import UserProfile, Synch, SynchMembership, Stream,\
    StreamMembership, Note, TextNote, ImageNote

# Create your views here.

"""

"""
class UserProfileViewSet (CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet): 
    permission_classes = [IsAuthenticated]
    def get_queryset(self): 
        return UserProfile.objects.select_related("user").all()
    
    def get_serializer_class(self):
        return UserProfileSerializer
    
    # to autofill the user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get', 'patch', 'put'], url_path='me', url_name='me')
    def me(self, request):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)

        if not profile:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(profile, data=request.data, partial=request.method == 'PATCH')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

    def get_permissions(self):
        # Define custom permissions based on request method
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
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
        profile = UserProfile.objects.get(user=user)
        try:
            # if on harmony/synchs/<synch_id>/members endpoint
            # memberships that are in this synch
            filter_condition = Q(synch_id=self.kwargs['synch_pk']) 
        except:
            # if on the harmony/synch_members endpoint
            # memberships that this user has or are part of the synchs this user is part of
            filter_condition = Q(member=profile) | Q(synch__members__member=profile)

        queryset = SynchMembership.objects\
                    .select_related("member", "member__user", "synch", \
                            "synch__creator", "synch__creator__user")\
                    .filter(filter_condition).distinct()
        return queryset
    
    def get_serializer_class(self):
        return SynchMembershipSerializer
    
    def get_permissions(self):
        # Define custom permissions based on request method
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsMemberOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    # remember that the serializer create function is also overriden
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(synch_id=self.kwargs['synch_pk'])

    # get the list of all the synch memberships that belong to the user
    @action(detail=False, methods=['get'], url_path='mine', url_name='mine')
    def mine(self, request, pk=None, synch_pk=None): 
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        queryset = SynchMembership.objects\
            .select_related("member", "member__user", "synch", \
                            "synch__creator", "synch__creator__user")\
            .filter(member=profile)
        serializer = SynchMembershipSerializer(queryset, many=True)
        return Response(serializer.data)
    
# end of SynchMembershipViewSet


"""

"""
class StreamViewSet (ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # get streams that are for everyone and the ones that the user is part of
        user = self.request.user
        profile = UserProfile.objects.get(user=user)

        try:
            # if on harmony/synchs/<synch_id>/streams endpoint
            # streams that are in this synch and is for everyone or the user is part of
            filter_condition = Q(synch_id=self.kwargs['synch_pk']) & (Q(membership_type=Stream.EVERYONE) | Q(members__member=profile))
            # for any for everyone stream in this synch this user does not have membership to, create the membership
            streams = Stream.objects.filter(Q(synch_id=self.kwargs['synch_pk']) & (Q(membership_type=Stream.EVERYONE) & ~Q(members__member__user=user)))
            for stream in streams: 
                StreamMembership.objects.create(stream_id=stream.id, member=profile)
        except:
            # if on the harmony/streams endpoint
            # streams that this user is part of and is for everyone or the user is part of
            filter_condition = Q(synch__members__member=profile) & (Q(membership_type=Stream.EVERYONE) | Q(members__member=profile))

        queryset = Stream.objects.filter(filter_condition).distinct()
        return queryset
    
    def get_serializer_class(self):
        return StreamSerializer
    
    def get_permissions(self):
        # Define custom permissions based on request method
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # get user making the request
        user = self.request.user
        # get the profile of this user
        profile = UserProfile.objects.get(user=user)

        with transaction.atomic():
            # save the new stream
            stream = serializer.save(creator=profile, synch_id=self.kwargs['synch_pk'])
            # make sure to create the stream membership (this stream + this user profile)
            # get the order first. it's gonna be the lowest order -1
            filter_condition = Q(stream__synch__id=self.kwargs['synch_pk']) & Q(status=StreamMembership.ACTIVE)
            lowest_order = StreamMembership.objects.filter(filter_condition).order_by("order").values_list('order', flat=True).first()
            new_order = (lowest_order if lowest_order else 0) - 1
            StreamMembership.objects.create(stream=stream, member=profile, status=StreamMembership.ACTIVE, order=new_order)

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
        # get the synch id of this stream
        stream = Stream.objects.get(id=pk)
        synch_id = synch_pk if synch_pk else stream.synch.id

        # return the result
        return Response({'stream_id':pk, 'synch_id':synch_id, 'content':stream_content})
    
    # get the list of all the active streams if inside a synch endpoint
    @action(detail=False, methods=['get'], url_path='my_active', url_name='my_active')
    def my_active(self, request, pk=None, synch_pk=None): 
        user = self.request.user
        profile = UserProfile.objects.get(user=user)

        try:
            # if on harmony/synchs/<synch_id>/streams/active endpoint
            # streams that are in this synch and is for everyone or the user is part of and active status of stream
            filter_condition = Q(synch_id=self.kwargs['synch_pk']) & Q(members__member=profile) & Q(members__status=StreamMembership.ACTIVE)
            queryset = Stream.objects.filter(filter_condition).distinct()
            serializer = StreamSerializer(queryset, many=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.data)



# end of StreamViewSet


"""

"""
class StreamMembershipViewSet (ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)

        try:
            # if on harmony/synchs/<synch_id>/my_stream_memberships endpoint
            # memberships that are in this synch
            filter_condition = Q(stream__synch__id=self.kwargs['synch_pk']) & Q(member=profile)
            # for any "everyone" stream in this synch this user does not have membership to, create the membership
            streams = Stream.objects.filter(Q(synch_id=self.kwargs['synch_pk']) & (Q(membership_type=Stream.EVERYONE) & ~Q(members__member__user=user)))
            for stream in streams: 
                StreamMembership.objects.create(stream_id=stream.id, member=profile)
        except:
            try:
                # if on harmony/streams/<stream_id>/members endpoint
                # memberships that are in this stream
                filter_condition = Q(stream_id=self.kwargs['stream_pk']) 
            except:
                # if on the harmony/stream_members endpoint
                # memberships that this user has or are part of the streams this user is part of
                filter_condition = Q(member=profile) | Q(stream__members__member=profile)
        # the filter condition might create duplicates so make sure to add distinct at the end
        queryset = StreamMembership.objects\
                    .select_related("stream", "stream__creator",\
                                    "stream__creator__user", "member",\
                                    "member__user")\
                    .filter(filter_condition).distinct()
        return queryset

    def get_serializer_class(self):
        return StreamMembershipSerializer
    
    def get_permissions(self):
        # Define custom permissions based on request method
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsMemberOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    # remember that the serializer create function is also overriden
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(stream_id=self.kwargs['stream_pk'])

    @action(detail=False, methods=['get'], url_path='get_from_stream/(?P<stream_id>[^/.]+)')
    def get_from_stream(self, request, stream_id=None):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        try:
            # get the stream in question
            stream = Stream.objects.select_related("synch").get(id=stream_id)
        
            # for any "everyone" stream in this synch this user does not have membership to, create the membership
            streams = Stream.objects.select_related("synch").filter(Q(synch_id=stream.synch.id) & (Q(membership_type=Stream.EVERYONE) & ~Q(members__member__user=user)))
            for stream in streams: 
                StreamMembership.objects.create(stream_id=stream.id, member=profile)
            
            # not get the stream membership the user need
            streamMembership = StreamMembership.objects.get(stream_id=stream_id, member=profile)
            serializer = self.get_serializer(streamMembership)
            return Response(serializer.data)
        except StreamMembership.DoesNotExist:
            return Response({"detail": "Stream Membership not found."}, status=status.HTTP_404_NOT_FOUND)

# end of StreamMembershipViewSet


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
        # get user making the request
        user = self.request.user
        # get the profile of this user
        profile = UserProfile.objects.get(user=user)

        try:
            # if on .../streams/<stream_id>/notes/<note_id>/texts/ endpoint
            filter_condition = Q(note_id=self.kwargs['note_pk']) 
        except:
            try:
                # if on .../streams/<stream_id>/texts/ endpoint
                filter_condition = Q(note__stream_id=self.kwargs['stream_pk']) 
            except:
                # if on the .../harmony/texts/ endpoint
                filter_condition = Q(note__stream__members__member=profile) 
        
        return TextNote.objects.filter(filter_condition).distinct()
    
    def get_serializer_class(self):
        return TextNoteSerializer
    
    def get_permissions(self):
        # Define custom permissions based on request method
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsNoteTakerOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # get user making the request
        user = self.request.user
        # get the profile of this user
        profile = UserProfile.objects.get(user=user)

        with transaction.atomic():
            try:
                # get note if on on .../streams/<stream_id>/notes/<note_id>/texts/ endpoint
                note = Note.objects.get(id=self.kwargs['note_pk'])
            except:
                try:
                    # create note if on .../streams/<stream_id>/texts/ endpoint
                    stream = Stream.objects.get(id=self.kwargs['stream_pk'])
                    note = Note.objects.create(stream=stream, taker=profile)
                except:
                    pass
            # perform saving
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




