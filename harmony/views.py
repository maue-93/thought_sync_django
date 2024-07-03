from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from .serializers import UserProfileSerializer, SynchSerializer, SynchMembershipSerializer
from .permissions import IsAdminOrReadOnly, IsSuperUserOrOwner, IsSuperUser
from .models import UserProfile, Synch, SynchMembership, Stream

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
        user = self.request.user
        return SynchMembership.objects.filter(member__user=user)
    
    def get_serializer_class(self):
        return SynchMembershipSerializer

# end of SynchMembershipViewSet


"""

"""
# class StreamViewSet (ModelViewSet):
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return SynchMembership.objects.filter(member__user=user)
    
#     def get_serializer_class(self):
#         return SynchMembershipSerializer

