from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comments_count']
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at', 'comments', 'comments_count']

    def get_comments_count(self, obj):
        """Get the number of comments on this post."""
        return obj.comments.count()


class PostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing posts (without nested comments)."""
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 'created_at', 'updated_at', 'comments_count']
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at', 'comments_count']

    def get_comments_count(self, obj):
        """Get the number of comments on this post."""
        return obj.comments.count()
