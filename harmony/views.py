from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import UserProfileSerializer
from .permissions import IsAdminOrReadOnly, IsSuperUserOrOwner, IsSuperUser
from .models import UserProfile

# JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5MzMwNzYwLCJpYXQiOjE3MTkyNDQzNjAsImp0aSI6ImQ5ZmFhNDZkZDc2ZTQxZmQ5NjFjMDFjODk5ZDM2YjcyIiwidXNlcl9pZCI6IjFjNWQ3OGFmLWExNDgtNDg2Ny1hM2U1LWVjNzkxZTZmOTMxOCJ9.B3IgcxGf_9MpZx8EqJbQpVN7FcAFOBHxZyzIGkjTCG4
# JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5MzM2Mzk4LCJpYXQiOjE3MTkyNDk5OTgsImp0aSI6ImU1N2VjMTdjNzU4ZjRhNDdiZTdkNTY2ZjM0YTEyM2ZjIiwidXNlcl9pZCI6ImEwNGNlZmMxLTUxNzMtNGFmNi1hZWEwLTY2N2Q0OThhZTI3YiJ9.pmegeZ5CRKWbEq1xl1HGEZTBwXOdNaamVgLE3GjpVu8
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
    
