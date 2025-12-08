from django.urls import path
from . import views

urlpatterns = [
    # User registration
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    # User login
    path('login/', views.UserLoginView.as_view(), name='login'),
    
    # User profile (view and update)
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    
    # List all users
    path('users/', views.UserListView.as_view(), name='user-list'),
]
