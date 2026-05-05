from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserFollowing

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture', 'password', 'followers_count']
        
    def get_followers_count(self, obj):
        return obj.followers.count() if hasattr(obj, 'followers') else 0
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            password= validated_data['password'],
        )
        return user

class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ['id', 'following_user', 'created_at']
        read_only_fields = ['id', 'created_at']
        