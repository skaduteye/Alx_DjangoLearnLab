# Create Operation - Book Model

## Django Shell Commands

To create a new Book instance using the Django shell:

```python
# Import the Book model
from bookshelf.models import Book

# Create a new book using the create() method
book1 = Book.objects.create(
    title="The Great Gatsby",
    author="F. Scott Fitzgerald",
    publication_year=1925
)

# Alternative: Create and save manually
book2 = Book(
    title="To Kill a Mockingbird",
    author="Harper Lee",
    publication_year=1960
)
book2.save()

# Verify the book was created
print(f"Created: {book1}")
print(f"Created: {book2}")
```

## Running the Commands

1. Open Django shell:
   ```bash
   python manage.py shell
   ```

2. Execute the commands above to create Book instances.
