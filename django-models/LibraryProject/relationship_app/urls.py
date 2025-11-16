from django.urls import path
from .views import list_books, LibraryDetailView  # old views for previous checks
from . import views  # module import for authentication views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Old views
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]

# Role-based URLs
path('admin-view/', views.admin_view, name='admin_view'),
path('librarian-view/', views.librarian_view, name='librarian_view'),
path('member-view/', views.member_view, name='member_view'),
