from rest_framework import serializers
from .models import User, Post, Like, Friendship

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'image_url', 'caption', 'created_at', 'likes_count', 'is_liked']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

class FriendshipSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)
    
    class Meta:
        model = Friendship
        fields = ['id', 'friend', 'created_at']