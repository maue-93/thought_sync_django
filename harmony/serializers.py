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
        fields = ["id", "user", "user_pk", "birthday", "bio", "picture"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user') and not request.user.is_superuser:
            self.fields['user_pk'].queryset = User.objects.filter(id=request.user.id)