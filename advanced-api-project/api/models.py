from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author model represents a book author.
    
    Fields:
        name: The full name of the author (max 100 characters)
    
    Relationships:
        One-to-Many with Book model - An author can have multiple books
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a published book.
    
    Fields:
        title: The title of the book (max 200 characters)
        publication_year: The year the book was published (integer)
        author: Foreign key relationship to Author model
    
    Relationships:
        Many-to-One with Author model - Each book has one author,
        but an author can have multiple books
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'  # Allows reverse lookup: author.books.all()
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
