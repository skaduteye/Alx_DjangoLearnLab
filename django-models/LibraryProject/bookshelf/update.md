# Update Operation - Book Model

## Django Shell Commands

```python
# Import the Book model
from bookshelf.models import Book

# Retrieve the book "1984"
book = Book.objects.get(title="1984")

# Update the title to "Nineteen Eighty-Four"
book.title = "Nineteen Eighty-Four"
book.save()

# Verify the update
print(f"Updated Title: {book.title}")

# Expected Output:
# Updated Title: Nineteen Eighty-Four
```
