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


class SynchSerializer (serializers.ModelSerializer):
    creator = UserProfileSerializer(read_only=True)
    class Meta:
        model = models.Synch
        fields = ["id", "name", "creator", "picture", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

# end of SynchSerializer


class SynchMembershipSerializer (serializers.ModelSerializer):
    # synch = SynchSerializer()
    # member = UserProfileSerializer()
    # synch_id = serializers.PrimaryKeyRelatedField(queryset=models.Synch.objects.all(), source='synch')
    member_id = serializers.PrimaryKeyRelatedField(queryset=models.UserProfile.objects.all(), source='member')

    class Meta:
        model = models.SynchMembership
        fields = ["id", "synch_id", "member_id"]
        read_only_fields = ["id", "synch_id"]

# end of SynchMembershipSerializer


class StreamSerializer (serializers.ModelSerializer):
    creator = UserProfileSerializer(read_only=True)
    # synch_id = serializers.PrimaryKeyRelatedField(queryset=models.Synch.objects.all(), source='synch')
    
    class Meta:
        model = models.Stream
        fields = ["id", "synch_id", "name", "creator", "created_at", "updated_at"]
        read_only_fields = ["id", "synch_id", "creator", "created_at", "updated_at"]

# end of StreamSerializer


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
        read_only_fields = ["id", "type", "created_at", "updated_at", "images"]

    def get_note_id (self, obj):
        return obj.id
# end of ImageNoteBulkSerializer
