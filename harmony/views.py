from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import UserProfileSerializer, SynchSerializer, SynchMembershipSerializer
from .permissions import IsAdminOrReadOnly, IsSuperUserOrOwner, IsSuperUser
from .models import UserProfile, Synch, SynchMembership

# Create your views here.

"""

"""
class UserProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self): 
        # only the user's profile
        return UserProfile.objects.select_related("user").filter(user=self.request.user)
    
    def get_serializer_class(self):
        return UserProfileSerializer
    
    # to autofill the user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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




