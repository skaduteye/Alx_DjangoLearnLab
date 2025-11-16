# Retrieve Operation - Book Model

## Django Shell Commands

```python
# Import the Book model
from bookshelf.models import Book

# Retrieve and display all attributes of the book "1984"
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")

# Expected Output:
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
```
