from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from app.models import Post, Like, Friendship
from app.serializers import PostSerializer
from app.services import RecommendationService


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
        Zwraca feed: najpierw posty znajomych, potem rekomendacje KNN
        """
        # Parametry paginacji
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))

        # Pobierz ID znajomych
        friends_ids = list(Friendship.objects.filter(
            user=request.user
        ).values_list('friend_id', flat=True))

        # Posty znajomych (sorted by recency)
        friends_posts = Post.objects.filter(
            user_id__in=friends_ids
        ).order_by('-created_at')

        friends_count = friends_posts.count()

        # Calculate if we need recommendations
        if offset < friends_count:
            # Still showing friends' posts
            posts_to_show = list(friends_posts[offset:offset + limit])
            remaining_slots = limit - len(posts_to_show)

            if remaining_slots > 0:
                # Need to fill with recommendations
                exclude_ids = set(friends_posts.values_list('id', flat=True))
                recommendations = self._get_knn_recommendations(
                    request.user,
                    remaining_slots,
                    exclude_ids
                )
                posts_to_show.extend(recommendations)
                source = 'mixed'
            else:
                source = 'friends'
        else:
            # Only show recommendations
            recommended_offset = offset - friends_count
            exclude_ids = set(friends_posts.values_list('id', flat=True))
            posts_to_show = self._get_knn_recommendations(
                request.user,
                limit,
                exclude_ids,
                offset=recommended_offset
            )
            source = 'recommended'

        serializer = self.get_serializer(posts_to_show, many=True)

        return Response({
            'results': serializer.data,
            'count': len(posts_to_show),
            'friends_count': friends_count,
            'source': source,
            'offset': offset,
            'limit': limit
        })

    def _get_knn_recommendations(self, user, limit, exclude_ids, offset=0):
        """
        Helper method to get KNN-based recommendations
        """
        rec_service = RecommendationService(k_neighbors=20)

        # Get more recommendations than needed to handle pagination
        fetch_limit = limit + offset + 50  # Buffer for filtering
        recommendations = rec_service.get_recommendations(
            user=user,
            limit=fetch_limit,
            exclude_post_ids=exclude_ids
        )

        # Apply offset and limit
        return recommendations[offset:offset + limit]

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