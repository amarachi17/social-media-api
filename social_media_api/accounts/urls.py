from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshview
from .views import RegisterUserView, UserProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/',  TokenRefreshview.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile')

]

