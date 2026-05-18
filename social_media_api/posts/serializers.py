from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 
            'author', 
            'title', 
            'content', 
            'created_at', 
            'updated_at', 
            'total_likes']
        
        read_only_fields = [
            'author', 
            'created_at',
            'updated_at'
        ]
        
    def get_total_likes(self, obj):
        return obj.likes.count() 
    
    def create(self, validated_data):
        request = self.context.get('request')

        return Post.objects.create(
            author= request.user, 
            **validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = [
            'id', 
            'post', 
            'author', 
            'content', 
            'created_at', 
            'updated_at']
        
        read_only_fields = [
            'author', 
            'created_at', 
            'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        return Comment.objects.create(
            author=request.user, 
            **validated_data)