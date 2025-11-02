# Delete Operation - Book Model

## Django Shell Commands

To delete Book instances from the database:

```python
# Import the Book model
from bookshelf.models import Book

# Method 1: Delete a single book by retrieving it first
book = Book.objects.get(id=1)
book_title = book.title
book.delete()
print(f"Deleted: {book_title}")

# Method 2: Delete using filter
Book.objects.filter(id=2).delete()

# Method 3: Delete multiple books matching a condition
deleted_count = Book.objects.filter(publication_year__lt=1900).delete()
print(f"Deleted {deleted_count[0]} books published before 1900")

# Method 4: Delete all books (use with caution!)
# Book.objects.all().delete()

# Verify deletion
remaining_books = Book.objects.all()
print(f"Remaining books: {remaining_books.count()}")
for book in remaining_books:
    print(f"  - {book}")
```

## Running the Commands

1. Open Django shell:
   ```bash
   python manage.py shell
   ```

2. Execute the commands above to delete Book instances.

## Warning
Be careful with delete operations, especially `all().delete()`, as they permanently remove data from the database!
