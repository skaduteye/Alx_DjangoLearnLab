from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Creates a new user and returns an authentication token.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get the token for the user
        token = Token.objects.get(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully.'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API view for user login.
    Authenticates user credentials and returns an authentication token.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Login successful.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials. Please check your username and password.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profile.
    Requires authentication.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the current authenticated user."""
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'user': serializer.data,
            'message': 'Profile updated successfully.'
        })


class UserListView(generics.ListAPIView):
    """
    API view for listing all users.
    Requires authentication.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class FollowUserView(generics.GenericAPIView):
    """
    API view for following a user.
    POST to follow the specified user.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def post(self, request, user_id):
        """Follow the user with the given user_id."""
        user_to_follow = get_object_or_404(User, id=user_id)
        
        # Cannot follow yourself
        if user_to_follow == request.user:
            return Response({
                'error': 'You cannot follow yourself.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following
        if request.user.following.filter(id=user_id).exists():
            return Response({
                'error': f'You are already following {user_to_follow.username}.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Add to following (which adds current user to target's followers)
        user_to_follow.followers.add(request.user)
        
        return Response({
            'message': f'You are now following {user_to_follow.username}.',
            'following': user_to_follow.username
        }, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    API view for unfollowing a user.
    POST to unfollow the specified user.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def post(self, request, user_id):
        """Unfollow the user with the given user_id."""
        user_to_unfollow = get_object_or_404(User, id=user_id)
        
        # Cannot unfollow yourself
        if user_to_unfollow == request.user:
            return Response({
                'error': 'You cannot unfollow yourself.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if not following
        if not request.user.following.filter(id=user_id).exists():
            return Response({
                'error': f'You are not following {user_to_unfollow.username}.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove from following
        user_to_unfollow.followers.remove(request.user)
        
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}.',
            'unfollowed': user_to_unfollow.username
        }, status=status.HTTP_200_OK)
