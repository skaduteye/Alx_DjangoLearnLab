from django.urls import path
from . import views

urlpatterns = [
    # List all notifications
    path('', views.NotificationListView.as_view(), name='notification-list'),
    
    # Get a specific notification
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    
    # Mark a notification as read
    path('<int:pk>/read/', views.MarkNotificationReadView.as_view(), name='notification-read'),
    
    # Mark all notifications as read
    path('mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='notifications-mark-all-read'),
    
    # Get unread notification count
    path('unread-count/', views.UnreadNotificationCountView.as_view(), name='notifications-unread-count'),
]
