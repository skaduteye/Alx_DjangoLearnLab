from rest_framework import viewsets, permissions, filters, generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, PostListSerializer, CommentSerializer


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
