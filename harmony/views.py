from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import UserProfileSerializer
from .permissions import IsAdminOrReadOnly, IsSuperUserOrOwner, IsSuperUser
from .models import UserProfile

# Create your views here.

class UserProfileViewSet(ModelViewSet):
    def get_queryset(self): 
        # select_related added to not repeat queries on user
        if self.request.user.is_superuser:
            return UserProfile.objects.select_related("user").all()
        return UserProfile.objects.select_related("user").filter(user=self.request.user)
        # return UserProfile.objects.select_related("user").all()
    def get_serializer_class(self):
        return UserProfileSerializer
    

def th ():
    return 0