from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# Create your views here.

class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    - Endpoint: GET /books/
    - Permissions: Read-only access for unauthenticated users
    - Returns: A list of all Book instances serialized with BookSerializer
    
    This view uses Django REST Framework's ListAPIView which provides
    a read-only endpoint for listing a collection of model instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access


class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by ID.
    
    - Endpoint: GET /books/<int:pk>/
    - Permissions: Read-only access for unauthenticated users
    - Returns: A single Book instance identified by primary key
    
    This view uses Django REST Framework's RetrieveAPIView which provides
    a read-only endpoint for retrieving a single model instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access


class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    - Endpoint: POST /books/create/
    - Permissions: Requires authentication
    - Request Body: JSON with title, publication_year, and author fields
    - Returns: The newly created Book instance
    
    This view uses Django REST Framework's CreateAPIView which provides
    a create-only endpoint. Custom validation is handled by the BookSerializer,
    including the check that publication_year is not in the future.
    
    Custom Behavior:
    - Only authenticated users can create books
    - Automatic validation through BookSerializer
    - Returns 201 Created on success with the created object
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication
    
    def perform_create(self, serializer):
        """
        Custom create method to add additional processing if needed.
        Currently saves the book instance after validation.
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    - Endpoint: PUT /books/<int:pk>/update/ or PATCH /books/<int:pk>/update/
    - Permissions: Requires authentication
    - Request Body: JSON with fields to update (PUT=full, PATCH=partial)
    - Returns: The updated Book instance
    
    This view uses Django REST Framework's UpdateAPIView which provides
    update functionality supporting both PUT (full update) and PATCH (partial update).
    
    Custom Behavior:
    - Only authenticated users can update books
    - Validates data through BookSerializer
    - Supports both full (PUT) and partial (PATCH) updates
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication
    
    def perform_update(self, serializer):
        """
        Custom update method to add additional processing if needed.
        Currently saves the updated book instance after validation.
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    - Endpoint: DELETE /books/<int:pk>/delete/
    - Permissions: Requires authentication
    - Returns: 204 No Content on successful deletion
    
    This view uses Django REST Framework's DestroyAPIView which provides
    delete functionality for a single model instance.
    
    Custom Behavior:
    - Only authenticated users can delete books
    - Returns 404 if book doesn't exist
    - Returns 204 No Content on successful deletion
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication
