from rest_framework import serializers
from .models import UserProfile
from core.serializers import UserCreateSerializer, UserSerializer
from core.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # used to link this profile to an existing user
    user_pk = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    class Meta:
        model = UserProfile
        fields = ["user", "user_pk", "bio", "picture"]