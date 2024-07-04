from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers.auth_serializers import CustomTokenObtainPairSerializer, DeactivateProfileSerializer, UserProfileSerializer, UserSerializer
from rest_framework import generics,permissions
from api.models.auth_models import User, UserProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView




class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile_data = {
                'user': user.id,
                'bio': '',  
                'profile_picture': None
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()

            user_data = UserSerializer(user).data
            return Response({"user": user_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'user_id'

    def get_object(self):
        user_id = self.kwargs.get(self.lookup_field)
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            raise NotFound("profile not found")
        return user_profile

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDeactivate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeactivateProfileSerializer


    def post(self, request, user_id):
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
            user_profile.is_active = False
            user_profile.save()
            return Response({"detail": "User profile deactivated."}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            raise NotFound("User profile not found")