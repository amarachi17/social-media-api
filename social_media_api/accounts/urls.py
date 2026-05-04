from django.urls import path
from .views import RegisterUserView, LoginView, FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterUserView, name='register'),
    path('login/', LoginView, name='login'),
    path('follow/<int:user_id>/',  FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user')

]

