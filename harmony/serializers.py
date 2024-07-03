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
    class Meta:
        model = models.SynchMembership
        fields = ["id", "synch", "member"]
        read_only_fields = ["id"]

# end of SynchMembershipSerializer

class StreamSerializer (serializers.ModelSerializer):
    creator = UserProfileSerializer(read_only=True)
    class Meta:
        model = models.Stream
        fields = ["id", "name", "creator"]
        read_only_fields = ["id"]
