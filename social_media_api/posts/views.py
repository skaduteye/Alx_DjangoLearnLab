from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostListSerializer, CommentSerializer
from notifications.models import Notification


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing posts.
    
    list: Get all posts (paginated)
    create: Create a new post
    retrieve: Get a specific post
    update: Update a post (owner only)
    partial_update: Partial update a post (owner only)
    destroy: Delete a post (owner only)
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use different serializers for list vs detail views."""
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """Set the author to the current user when creating a post."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing comments.
    
    list: Get all comments (paginated)
    create: Create a new comment
    retrieve: Get a specific comment
    update: Update a comment (owner only)
    partial_update: Partial update a comment (owner only)
    destroy: Delete a comment (owner only)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        """Set the author to the current user when creating a comment."""
        serializer.save(author=self.request.user)


class FeedView(generics.ListAPIView):
    """
    API view for retrieving the user's feed.
    Returns posts from users that the current user follows,
    ordered by creation date (most recent first).
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return posts from users that the current user follows.
        """
        # Get the users that the current user is following
        following_users = self.request.user.following.all()
        
        # Return posts from those users, ordered by most recent
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class LikePostView(APIView):
    """
    API view for liking a post.
    POST to like the specified post.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Like the post with the given pk."""
        post = get_object_or_404(Post, pk=pk)
        
        # Check if already liked
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            return Response({
                'error': 'You have already liked this post.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create notification for the post author (if not liking own post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            )
        
        return Response({
            'message': f'You have liked the post "{post.title}".',
            'post_id': post.id,
            'likes_count': post.likes.count()
        }, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    """
    API view for unliking a post.
    POST to unlike the specified post.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Unlike the post with the given pk."""
        post = get_object_or_404(Post, pk=pk)
        
        # Try to get the like
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            
            return Response({
                'message': f'You have unliked the post "{post.title}".',
                'post_id': post.id,
                'likes_count': post.likes.count()
            }, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({
                'error': 'You have not liked this post.'
            }, status=status.HTTP_400_BAD_REQUEST)
