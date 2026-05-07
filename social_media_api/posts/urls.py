from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView

router = DefaultRouter()
router.register(r'', PostViewSet, basename= 'posts')

urlpatterns = [
    path('', include(router.urls)),

    path(
        '<int:post_pk>/comments/',
        CommentViewSet.as_view({
            'get': 'list', 
            'post': 'create'
            }),
            name='comment-list'
        ),
    path(
        '<int:post_pk>/comments/<int:pk>/',
        CommentViewSet.as_view({
            'get': 'retrieve', 
            'put': 'update', 
            'delete': 'destroy'
            }),
            name='comment-detail'
        ),
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]
