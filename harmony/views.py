from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import UserProfileSerializer
from .permissions import IsAdminOrReadOnly, IsSuperUserOrOwner, IsSuperUser
from .models import UserProfile

# Create your views here.

class UserProfileViewSet(ModelViewSet):
    def get_queryset(self): 
        # if super user query all
        if self.request.user.is_superuser:
            # select_related added to not repeat queries on user
            return UserProfile.objects.select_related("user").all()
        # if user logged in, query their profile
        return UserProfile.objects.select_related("user").filter(user=self.request.user)
    def get_serializer_class(self):
        return UserProfileSerializer
    
    # to add a context to use in serializer
    def get_serializer_context(self):
        # Pass the request context to the serializer
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
        })
        return context
    
