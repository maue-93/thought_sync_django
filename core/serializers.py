from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

"""
Eliso
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxOTE1NTAxMSwiaWF0IjoxNzE4OTgyMjExLCJqdGkiOiI1ZmQ2MzkwNDhjNjA0ZTFiOTkyYzJjMDI2ZDBiOGViMCIsInVzZXJfaWQiOiIxYzVkNzhhZi1hMTQ4LTQ4NjctYTNlNS1lYzc5MWU2ZjkzMTgifQ._tM5H0r_c1_04y8YbBVQ0dTcJByXb5jb1ZWMaPnuwdc",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5MDY4NjExLCJpYXQiOjE3MTg5ODIyMTEsImp0aSI6IjZmNmE2YzQ2MTQ5NTQxODg5ZDQ1OTRiNTU3MTg1OWQ3IiwidXNlcl9pZCI6IjFjNWQ3OGFmLWExNDgtNDg2Ny1hM2U1LWVjNzkxZTZmOTMxOCJ9.BfAR_7_eeNjGGwZzs2oWkONzr7zFmiCaHIqDNBctBIY"
}
"""

"""
morazare 
JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5MDY2NzE1LCJpYXQiOjE3MTg5ODAzMTUsImp0aSI6IjRhODAxYzExMDY0ZTQ1Mjg5ZDhkODc4OTAxMWYxZDg5IiwidXNlcl9pZCI6IjNhYzAwMzMxLWI1MTktNDA0Ni04ZDg3LTgxZTVmNTlkNWU0MSJ9.yQZeJHMb_VAxvPFuSx7a5jp7iezKEH5V_jM2iWw1O1I
"""


"""
    USES : - To create a user

    TO DO : - do we need id in the create serializer
"""
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
# end of UserCreateSerializer

"""

"""
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['username', 'email', 'first_name', 'last_name']