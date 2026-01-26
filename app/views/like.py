from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models import Like
from app.serializers import LikeSerializer

class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]