"""
URL Configuration for the API app

This module defines all the URL patterns for the Book API endpoints.
Each endpoint is mapped to a specific generic view that handles CRUD operations.

URL Patterns:
- /books/ - List all books (GET) - Public access
- /books/<int:pk>/ - Retrieve a single book (GET) - Public access
- /books/create/ - Create a new book (POST) - Authenticated users only
- /books/<int:pk>/update/ - Update a book (PUT/PATCH) - Authenticated users only
- /books/<int:pk>/delete/ - Delete a book (DELETE) - Authenticated users only
"""

from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # List all books - Public access
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve a single book by ID - Public access
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book - Requires authentication
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book - Requires authentication
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update-alt'),
    
    # Delete a book - Requires authentication
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete-alt'),
]
