from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    API view for listing all notifications for the current user.
    Returns notifications ordered by timestamp (most recent first).
    Unread notifications are highlighted.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return notifications for the current user."""
        return Notification.objects.filter(recipient=self.request.user)


class NotificationDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving a specific notification.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only notifications belonging to the current user."""
        return Notification.objects.filter(recipient=self.request.user)


class MarkNotificationReadView(APIView):
    """
    API view for marking a notification as read.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Mark the notification as read."""
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
            notification.read = True
            notification.save()
            return Response({
                'message': 'Notification marked as read.',
                'notification_id': pk
            }, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({
                'error': 'Notification not found.'
            }, status=status.HTTP_404_NOT_FOUND)


class MarkAllNotificationsReadView(APIView):
    """
    API view for marking all notifications as read.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Mark all notifications for the current user as read."""
        updated_count = Notification.objects.filter(
            recipient=request.user,
            read=False
        ).update(read=True)
        
        return Response({
            'message': f'{updated_count} notifications marked as read.'
        }, status=status.HTTP_200_OK)


class UnreadNotificationCountView(APIView):
    """
    API view for getting the count of unread notifications.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Return the count of unread notifications."""
        count = Notification.objects.filter(
            recipient=request.user,
            read=False
        ).count()
        
        return Response({
            'unread_count': count
        }, status=status.HTTP_200_OK)
