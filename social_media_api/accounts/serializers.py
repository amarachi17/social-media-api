from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import UserFollowing

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            'id', 
            'username', 
            'bio', 
            'profile_picture', 
            'password', 
            'followers_count'
        ]
            
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def get_followers_count(self, obj):
        return obj.followers.count() 
        
    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        Token.objects.create(user=user)

        return user

class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        
        fields = [
            'id', 
            'following_user', 
            'created_at'
        ]

        read_only_fields = [
            'id',
            'created_at'
        ]
        