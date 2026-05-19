from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserFollowingSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from .models import CustomUser, UserFollowing
from .serializers import UserSerializer, UserFollowingSerializer



User = get_user_model()

# Create your views here.
class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes =[AllowAny]

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class FollowUserView(generics.GenericAPIView):
    serializer_class = UserFollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        following_user_id = self.kwargs.get('user_id')

        following_user = generics.get_object_or_404(
           User,
           id = following_user_id
        )

        if request.user == following_user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        _, created =  UserFollowing.objects.get_or_create(user=request.user, following_user=following_user)

        if created:
            return Response({'detail': 'Successfully followed user.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)
        

class UnfollowUserView(generics.GenericAPIView):
    serializer_class = UserFollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        following_user_id = self.kwargs.get('user_id')
        try:
            following_user = User.objects.get(id=following_user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == following_user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            follow_instance = UserFollowing.objects.get(user=request.user, following_user=following_user)
            follow_instance.delete()

            return Response({'detail': 'Successfully unfollowed user.'}, status=status.HTTP_200_OK)
        except UserFollowing.DoesNotExist:
            return Response({'detail': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)
        
       
        