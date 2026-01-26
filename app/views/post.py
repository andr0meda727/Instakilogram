from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from app.models import Post, Like, Friendship
from app.serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """
        Zwraca feed: najpierw posty znajomych, potem proponowane
        """
        # Pobierz ID znajomych
        friends_ids = Friendship.objects.filter(
            user=request.user
        ).values_list('friend_id', flat=True)
        
        # Posty znajomych
        friends_posts = Post.objects.filter(
            user_id__in=friends_ids
        ).order_by('-created_at')
        
        # Posty proponowane (nie od znajomych i nie własne)
        recommended_posts = Post.objects.exclude(
            Q(user_id__in=friends_ids) | Q(user=request.user)
        ).order_by('-created_at')
        
        # Parametry paginacji
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        
        # Łączenie postów: najpierw znajomi, potem proponowane
        all_posts = list(friends_posts) + list(recommended_posts)
        paginated_posts = all_posts[offset:offset + limit]
        
        serializer = self.get_serializer(paginated_posts, many=True)
        
        return Response({
            'results': serializer.data,
            'count': len(all_posts),
            'friends_count': friends_posts.count(),
            'recommended_count': recommended_posts.count()
        })
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """
        Endpoint dla zewnętrznego skryptu KNN do pobrania danych
        Zwraca posty z informacjami o polubeniach użytkownika
        """
        user_liked_posts = Like.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True)
        
        all_posts = Post.objects.all()
        serializer = self.get_serializer(all_posts, many=True)
        
        return Response({
            'user_id': request.user.id,
            'liked_posts': list(user_liked_posts),
            'all_posts': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Polub post"""
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already_liked'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Odlub post"""
        post = self.get_object()
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        
        if deleted:
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'not_liked'}, status=status.HTTP_400_BAD_REQUEST)
