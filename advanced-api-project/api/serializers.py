from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles serialization and deserialization of Book instances,
    converting between JSON and Python objects.
    
    Fields:
        - All fields from the Book model (id, title, publication_year, author)
    
    Custom Validation:
        - Ensures publication_year is not in the future
    """
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        
        Args:
            value: The publication year to validate
            
        Returns:
            The validated publication year
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer includes a nested representation of all books written by the author,
    demonstrating a one-to-many relationship serialization.
    
    Fields:
        - name: The author's name
        - books: A nested list of all books by this author (read-only)
    
    Relationship Handling:
        The 'books' field uses the BookSerializer to serialize all related Book instances.
        This creates a nested JSON structure where each author object includes all their books.
        The field is read-only because books are created separately and linked via foreign key.
    """
    
    # Nested serializer to include all books by this author
    # Uses the related_name='books' defined in the Book model's ForeignKey
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
