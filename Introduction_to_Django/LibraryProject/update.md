# Update Operation - Book Model

## Django Shell Commands

To update existing Book instances:

```python
# Import the Book model
from bookshelf.models import Book

# Method 1: Retrieve and update a single book
book = Book.objects.get(id=1)
book.title = "The Great Gatsby (Updated Edition)"
book.publication_year = 1926
book.save()
print(f"Updated book: {book}")

# Method 2: Update using update() method for single object
Book.objects.filter(id=1).update(
    author="Francis Scott Fitzgerald"
)

# Method 3: Bulk update multiple books
Book.objects.filter(publication_year__lt=1950).update(
    publication_year=1950
)

# Verify the updates
updated_book = Book.objects.get(id=1)
print(f"Final state: {updated_book.title} by {updated_book.author} ({updated_book.publication_year})")
```

## Running the Commands

1. Open Django shell:
   ```bash
   python manage.py shell
   ```

2. Execute the commands above to update Book instances.
