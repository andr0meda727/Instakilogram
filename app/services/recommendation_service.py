"""
KNN-based recommendation service for Instakilogram using scikit-learn
Implements real-time computation with sklearn's NearestNeighbors
"""
import numpy as np
from typing import List, Set, Tuple
from collections import defaultdict
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Count
from app.models import User, Post, Like


class RecommendationService:
    """
    Real-time KNN recommendation system using scikit-learn
    that finds similar users based on post likes.
    """

    def __init__(self, k_neighbors: int = 20, metric: str = 'cosine'):
        """
        Initialize the recommendation service.

        Args:
            k_neighbors: Number of similar users to consider for recommendations
            metric: Distance metric for KNN ('cosine', 'jaccard', 'euclidean')
        """
        self.k_neighbors = k_neighbors
        self.metric = metric

    def get_recommendations(
        self,
        user: User,
        limit: int = 20,
        exclude_post_ids: Set[int] = None
    ) -> List[Post]:
        """
        Get recommended posts for a user based on KNN algorithm using sklearn.

        Args:
            user: The user to get recommendations for
            limit: Maximum number of posts to return
            exclude_post_ids: Set of post IDs to exclude (already seen/liked)

        Returns:
            List of recommended Post objects
        """
        if exclude_post_ids is None:
            exclude_post_ids = set()

        # 1. Get user's liked posts
        user_liked_posts = set(
            Like.objects.filter(user=user).values_list('post_id', flat=True)
        )

        # Add user's liked posts to exclusion list
        exclude_post_ids.update(user_liked_posts)

        # Also exclude user's own posts
        user_own_posts = set(
            Post.objects.filter(user=user).values_list('id', flat=True)
        )
        exclude_post_ids.update(user_own_posts)

        # Handle cold start - if user has no likes
        if not user_liked_posts:
            return self._get_popular_posts(limit, exclude_post_ids)

        # 2. Build user-item matrix and find similar users
        similar_users = self._find_similar_users_sklearn(user, user_liked_posts)

        if not similar_users:
            # No similar users found, return popular posts
            return self._get_popular_posts(limit, exclude_post_ids)

        # 3. Get candidate posts from similar users
        recommended_posts = self._get_posts_from_similar_users(
            similar_users,
            exclude_post_ids,
            limit
        )

        return recommended_posts

    def _build_user_item_matrix(self) -> Tuple[np.ndarray, List[int], List[int]]:
        """
        Build a user-item interaction matrix.

        Returns:
            matrix: Sparse binary matrix (users x posts)
            user_ids: List of user IDs corresponding to matrix rows
            post_ids: List of post IDs corresponding to matrix columns
        """
        # Get all likes
        likes = Like.objects.all().values_list('user_id', 'post_id')

        if not likes:
            return np.array([]), [], []

        # Get unique users and posts
        user_ids = sorted(set(User.objects.filter(likes__isnull=False).values_list('id', flat=True)))
        post_ids = sorted(set(Post.objects.filter(likes__isnull=False).values_list('id', flat=True)))

        # Create mapping dictionaries
        user_idx = {uid: idx for idx, uid in enumerate(user_ids)}
        post_idx = {pid: idx for idx, pid in enumerate(post_ids)}

        # Initialize matrix
        matrix = np.zeros((len(user_ids), len(post_ids)), dtype=np.float32)

        # Fill matrix
        for user_id, post_id in likes:
            if user_id in user_idx and post_id in post_idx:
                matrix[user_idx[user_id], post_idx[post_id]] = 1.0

        return matrix, user_ids, post_ids

    def _find_similar_users_sklearn(
        self,
        target_user: User,
        target_user_likes: Set[int]
    ) -> List[Tuple[User, float]]:
        """
        Find K most similar users using sklearn's NearestNeighbors.

        Args:
            target_user: User to find similar users for
            target_user_likes: Set of post IDs the target user has liked

        Returns:
            List of (User, similarity_score) tuples, sorted by similarity
        """
        # Build user-item matrix
        matrix, user_ids, post_ids = self._build_user_item_matrix()

        if matrix.size == 0 or target_user.id not in user_ids:
            return []

        # Find target user's index
        target_idx = user_ids.index(target_user.id)

        # Configure KNN model
        # For cosine similarity, we need to use 'cosine' metric
        # n_neighbors + 1 because the user itself will be in results
        knn = NearestNeighbors(
            n_neighbors=min(self.k_neighbors + 1, len(user_ids)),
            metric=self.metric,
            algorithm='brute'  # Use brute force for small datasets
        )

        # Fit the model
        knn.fit(matrix)

        # Find nearest neighbors
        distances, indices = knn.kneighbors(
            matrix[target_idx].reshape(1, -1),
            n_neighbors=min(self.k_neighbors + 1, len(user_ids))
        )

        # Convert distances to similarities
        similarities = []
        for dist, idx in zip(distances[0], indices[0]):
            # Skip the user itself
            if idx == target_idx:
                continue

            # Convert distance to similarity
            if self.metric == 'cosine':
                # Cosine distance is 1 - cosine similarity
                similarity = 1 - dist
            elif self.metric == 'euclidean':
                # Convert euclidean distance to similarity
                similarity = 1 / (1 + dist)
            else:
                # For other metrics, use inverse distance
                similarity = 1 / (1 + dist)

            # Get user object
            similar_user_id = user_ids[idx]
            similar_user = User.objects.get(id=similar_user_id)

            similarities.append((similar_user, float(similarity)))

        return similarities

    def _get_posts_from_similar_users(
        self,
        similar_users: List[Tuple[User, float]],
        exclude_post_ids: Set[int],
        limit: int
    ) -> List[Post]:
        """
        Get posts liked by similar users, scored by how many similar users liked them.

        Args:
            similar_users: List of (User, similarity_score) tuples
            exclude_post_ids: Post IDs to exclude
            limit: Maximum number of posts to return

        Returns:
            List of recommended Post objects
        """
        # Count how many similar users liked each post
        post_scores = defaultdict(float)
        post_ids_to_consider = set()

        for similar_user, similarity_score in similar_users:
            # Get posts liked by this similar user
            liked_post_ids = Like.objects.filter(
                user=similar_user
            ).values_list('post_id', flat=True)

            for post_id in liked_post_ids:
                if post_id not in exclude_post_ids:
                    # Score is weighted by user similarity
                    post_scores[post_id] += similarity_score
                    post_ids_to_consider.add(post_id)

        if not post_scores:
            return []

        # Sort posts by score (descending)
        sorted_post_ids = sorted(
            post_scores.keys(),
            key=lambda pid: post_scores[pid],
            reverse=True
        )[:limit]

        # Fetch Post objects maintaining the score order
        posts = Post.objects.filter(id__in=sorted_post_ids)

        # Create a mapping for quick lookup
        posts_dict = {post.id: post for post in posts}

        # Return posts in score order
        ordered_posts = [posts_dict[pid] for pid in sorted_post_ids if pid in posts_dict]

        return ordered_posts

    def _get_popular_posts(
        self,
        limit: int,
        exclude_post_ids: Set[int]
    ) -> List[Post]:
        """
        Fallback method to get popular posts when no recommendations are available.
        Returns posts with most likes.

        Args:
            limit: Maximum number of posts to return
            exclude_post_ids: Post IDs to exclude

        Returns:
            List of popular Post objects
        """
        posts = Post.objects.exclude(
            id__in=exclude_post_ids
        ).annotate(
            like_count=Count('likes')
        ).order_by('-like_count', '-created_at')[:limit]

        return list(posts)

    def get_user_similarity(self, user1: User, user2: User) -> float:
        """
        Calculate similarity between two users using sklearn.
        Useful for debugging and analytics.

        Args:
            user1: First user
            user2: Second user

        Returns:
            Similarity score between 0 and 1
        """
        # Build matrix
        matrix, user_ids, post_ids = self._build_user_item_matrix()

        if user1.id not in user_ids or user2.id not in user_ids:
            return 0.0

        # Get user vectors
        idx1 = user_ids.index(user1.id)
        idx2 = user_ids.index(user2.id)

        vec1 = matrix[idx1].reshape(1, -1)
        vec2 = matrix[idx2].reshape(1, -1)

        # Calculate cosine similarity
        similarity = cosine_similarity(vec1, vec2)[0][0]

        return float(similarity)