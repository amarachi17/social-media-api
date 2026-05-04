from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, generics, status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import filters
from django.contrib.auth import get_user_model 
from rest_framework.permissions import IsAuthenticated
from .models import Post, Like
from notifications.models import Notification
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

User = get_user_model()
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serilaizer):
        serilaizer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_querset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'message': 'You have liked this post. '}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user != post.author:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            )
        return Response({'message': 'Post liked.'}, status=status.HTTP_201_CREATED)
    
class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        like = Like.objects.get(user=user, post=post).first()
        if not like:
            return Response({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        
        return Response({'message': 'Post unliked..'}, status=status.HTTP_204_NO_CONTENT)
        
