from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer

# Create your views here.

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of books.
    Requires authentication to access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Book model.
    - List and Retrieve: Available to authenticated users
    - Create, Update, Delete: Restricted to authenticated users
    
    Authentication required via Token Authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can perform CRUD operations
