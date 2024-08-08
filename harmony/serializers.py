from rest_framework import serializers
from . import models
from core.serializers import UserCreateSerializer, UserSerializer
from core.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = models.UserProfile
        fields = ["id", "user", "birthday", "bio", "picture"]
        read_only_fields = ["id"]
    
# end of UserProfileSerializer

class ForSynchSerializerOnlyNoteSerializer (serializers.ModelSerializer):
    taker = UserProfileSerializer(read_only=True)
    class Meta:
        model = models.Note
        fields = ["id", "stream_id", "taker", "created_at", "updated_at", "text", "images"]
        read_only_fields = ["id", "taker", "created_at", "updated_at", "text", "images"]
        
# end of ForSynchSerializerOnlyNoteSerializer

class SynchSerializer (serializers.ModelSerializer):
    creator = UserProfileSerializer(read_only=True)
    last_note = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Synch
        fields = ["id", "name", "creator", "picture", "created_at", "updated_at", "last_note"]
        read_only_fields = ["id", "created_at", "updated_at", "last_note"]

    def get_last_note (self, obj):
        last_note_obj = models.Note.objects.filter(stream__synch=obj).order_by('-created_at').first()
        if last_note_obj:
            return ForSynchSerializerOnlyNoteSerializer(last_note_obj).data
        return None

# end of SynchSerializer


class SynchMembershipSerializer (serializers.ModelSerializer):
    synch = SynchSerializer(read_only=True)
    member = UserProfileSerializer(read_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = models.SynchMembership
        fields = ["id", "synch_id", "created_at", "updated_at", "synch", "member", "username"]
        read_only_fields = ["id", "synch_id", "created_at", "updated_at", "synch", "member"]

    # remember that the viewset perform_create function is also overriden
    def create(self, validated_data):
        username = validated_data.pop('username')
        try:
            member = models.UserProfile.objects.get(user__username=username)
        except models.UserProfile.DoesNotExist:
            raise serializers.ValidationError({"username": "User with this username does not exist."})

        validated_data['member'] = member
        return super().create(validated_data)

# end of SynchMembershipSerializer


class StreamSerializer (serializers.ModelSerializer):
    creator = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = models.Stream
        fields = ["id", "name", "created_at", "updated_at", "membership_type", "synch_id", "creator"] 
        read_only_fields = ["id","created_at", "updated_at", "membership_type", "synch_id", "creator"]

# end of StreamSerializer


class StreamMembershipSerializer (serializers.ModelSerializer):
    stream = StreamSerializer(read_only=True)
    member = UserProfileSerializer(read_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = models.StreamMembership
        fields = ['id', "stream_id", "stream", "member", "order", "status", "username", "created_at", "updated_at"]
        read_only_fields = ["id", "stream_id", "stream", "member", "created_at", "updated_at"]

    # remember that the viewset perform_create function is also overriden
    def create(self, validated_data):
        username = validated_data.pop('username')
        try:
            member = models.UserProfile.objects.get(user__username=username)
        except models.UserProfile.DoesNotExist:
            raise serializers.ValidationError({"username": "User with this username does not exist."})

        validated_data['member'] = member
        return super().create(validated_data)
    
# end of StreamMembershipSerializer


class NoteSerializer (serializers.ModelSerializer):
    taker = UserProfileSerializer(read_only=True)
    class Meta:
        model = models.Note
        fields = ["id", "stream_id", "taker", "created_at", "updated_at"]
        read_only_fields = ["id", "taker", "created_at", "updated_at"]
        
# end of NoteSerializer


class TextNoteSerializer (serializers.ModelSerializer):
    type = serializers.CharField(default="text", read_only=True)
    note = NoteSerializer(read_only=True)
    class Meta:
        model = models.TextNote
        fields = ["id", "type", "created_at", "updated_at", "note_id", "note", "text"]
        read_only_fields = ["id", "type", "created_at", "updated_at", "note_id"]

# end of TextNoteSerializer


class ImageNoteSerializer (serializers.ModelSerializer):
    note = NoteSerializer(read_only=True)
    class Meta:
        model = models.ImageNote
        fields = ["id", "created_at", "updated_at", "note", "image"]
        read_only_fields = ["id", "created_at", "updated_at"]

# end of ImageNoteSerializer


class ImageNoteBulkSerializer (serializers.ModelSerializer):
    note_id = serializers.SerializerMethodField()
    type = serializers.CharField(default="images", read_only=True)
    images = ImageNoteSerializer(many=True)
    class Meta:
        model = models.Note
        fields = ["note_id", "type", "created_at", "updated_at", "images"]
        read_only_fields = ["note_id", "type", "created_at", "updated_at", "images"]

    def get_note_id (self, obj):
        return obj.id
# end of ImageNoteBulkSerializer
