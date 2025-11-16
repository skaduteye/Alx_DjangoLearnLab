# Delete Operation - Book Model

## Django Shell Commands

```python
# Import the Book model
from bookshelf.models import Book

# Delete the book "Nineteen Eighty-Four" (previously "1984")
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by retrieving all books
all_books = Book.objects.all()
print(f"All books: {all_books}")

# Expected Output:
# All books: <QuerySet []>
# The QuerySet is empty, confirming the book has been deleted.
```
