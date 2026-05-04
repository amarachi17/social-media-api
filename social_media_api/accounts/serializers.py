from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import CustomUser, UserFollowing

User = get_user_model().objects.create_user

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        # user = CustomUser.objects.create_user(
        #     username=validated_data['username'],
        #     email=validated_data.get('email', ''),
        #     password=validated_data['password']
        # )
        return user

class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ['id', 'following_user', 'created_at']
        read_only_fields = ['id', 'created_at']
        