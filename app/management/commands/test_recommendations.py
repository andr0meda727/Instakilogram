"""
Management command to test the KNN recommendation system
Works with both vanilla and sklearn versions
Usage: python manage.py test_recommendations <username>
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.services import RecommendationService
from app.models import Like, Post

User = get_user_model()


class Command(BaseCommand):
    help = 'Test the KNN recommendation system for a specific user'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='Username to generate recommendations for'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Number of recommendations to generate'
        )
        parser.add_argument(
            '--k',
            type=int,
            default=20,
            help='Number of similar users to consider (K in KNN)'
        )

    def handle(self, *args, **options):
        username = options['username']
        limit = options['limit']
        k = options['k']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'\n=== Testing Recommendations for {username} ===\n')
        )

        # Show user's liked posts
        user_likes = Like.objects.filter(user=user).select_related('post', 'post__user')
        self.stdout.write(f'User has liked {user_likes.count()} posts:')
        for like in user_likes[:5]:
            self.stdout.write(
                f'  - Post #{like.post.id} by @{like.post.user.username}: "{like.post.caption[:50]}..."'
            )
        if user_likes.count() > 5:
            self.stdout.write(f'  ... and {user_likes.count() - 5} more')

        self.stdout.write('')

        # Get recommendations
        rec_service = RecommendationService(k_neighbors=k)
        recommendations = rec_service.get_recommendations(user, limit=limit)

        self.stdout.write(
            self.style.SUCCESS(f'\n=== Top {len(recommendations)} Recommendations ===\n')
        )

        if not recommendations:
            self.stdout.write(
                self.style.WARNING('No recommendations found. User may need more likes or similar users.')
            )
            return

        for i, post in enumerate(recommendations, 1):
            likes_count = post.likes.count()
            self.stdout.write(
                f'{i}. Post #{post.id} by @{post.user.username}'
            )
            self.stdout.write(f'   Caption: "{post.caption[:60]}..."')
            self.stdout.write(f'   Likes: {likes_count}')
            self.stdout.write('')

        # Show similar users (for debugging) - check which method exists
        user_liked_posts = set(user_likes.values_list('post_id', flat=True))
        if user_liked_posts:
            # Try to get similar users - handle both vanilla and sklearn versions
            try:
                # Try sklearn version first
                if hasattr(rec_service, '_find_similar_users_sklearn'):
                    similar_users = rec_service._find_similar_users_sklearn(user, user_liked_posts)
                # Try vanilla version
                elif hasattr(rec_service, '_find_similar_users'):
                    similar_users = rec_service._find_similar_users(user, user_liked_posts)
                else:
                    similar_users = []

                if similar_users:
                    self.stdout.write(
                        self.style.SUCCESS(f'\n=== Top {min(5, len(similar_users))} Similar Users ===\n')
                    )

                    for similar_user, similarity in similar_users[:5]:
                        self.stdout.write(
                            f'@{similar_user.username} (similarity: {similarity:.3f})'
                        )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'\nCould not fetch similar users: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n=== Test Complete ===\n')
        )