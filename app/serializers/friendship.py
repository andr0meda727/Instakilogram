from rest_framework import serializers
from app.models import Friendship
from .user import UserSerializer

class FriendshipSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)
    
    class Meta:
        model = Friendship
        fields = ['id', 'friend', 'created_at']