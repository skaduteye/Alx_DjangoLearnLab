# Create Operation - Book Model

## Django Shell Commands

```python
# Import the Book model
from bookshelf.models import Book

# Create a Book instance with title "1984", author "George Orwell", and publication year 1949
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Expected Output: <Book: 1984>
# The book has been successfully created with the specified attributes.
```
