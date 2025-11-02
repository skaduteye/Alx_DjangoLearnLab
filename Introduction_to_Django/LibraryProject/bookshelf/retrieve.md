# Retrieve Operation - Book Model

## Django Shell Commands

To retrieve Book instances from the database:

```python
# Import the Book model
from bookshelf.models import Book

# Retrieve all books
all_books = Book.objects.all()
print("All books:", all_books)

# Retrieve a specific book by ID
book = Book.objects.get(id=1)
print(f"Book with ID 1: {book}")

# Retrieve books by filter
books_by_author = Book.objects.filter(author="F. Scott Fitzgerald")
print(f"Books by F. Scott Fitzgerald: {books_by_author}")

# Retrieve books published after a certain year
recent_books = Book.objects.filter(publication_year__gte=1950)
print(f"Books published after 1950: {recent_books}")

# Get the first book
first_book = Book.objects.first()
print(f"First book: {first_book}")

# Count total books
total_books = Book.objects.count()
print(f"Total books: {total_books}")
```

## Running the Commands

1. Open Django shell:
   ```bash
   python manage.py shell
   ```

2. Execute the commands above to retrieve Book instances.
