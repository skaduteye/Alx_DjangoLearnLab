# Advanced API Project - Django REST Framework

A comprehensive Django REST Framework project demonstrating custom views, generic views, nested serializers, and authentication/permissions.

## Project Overview

This project provides a RESTful API for managing books and authors with the following features:
- Custom serializers with nested relationships
- Generic views for CRUD operations
- Token-based authentication
- Role-based permissions
- Custom validation
- **Advanced filtering, searching, and ordering capabilities**

## Models

### Author
- `name`: CharField - The author's name

### Book
- `title`: CharField - The book's title
- `publication_year`: IntegerField - Year of publication
- `author`: ForeignKey - Relationship to Author model

**Relationship**: One-to-Many (One author can have multiple books)

## API Endpoints

### Public Endpoints (No Authentication Required)

#### 1. List All Books
- **URL**: `/api/books/`
- **Method**: `GET`
- **Description**: Retrieve a list of all books with filtering, searching, and ordering support
- **Response**: 200 OK with array of book objects
- **Query Parameters**:
  - `title`: Filter by exact title
  - `author__name`: Filter by author name
  - `publication_year`: Filter by publication year
  - `search`: Search in title and author name
  - `ordering`: Order by field (prefix with `-` for descending)
- **Examples**:
  ```bash
  # Get all books
  curl http://127.0.0.1:8000/api/books/
  
  # Filter by publication year
  curl http://127.0.0.1:8000/api/books/?publication_year=1997
  
  # Filter by author name
  curl "http://127.0.0.1:8000/api/books/?author__name=J.K. Rowling"
  
  # Search for books
  curl http://127.0.0.1:8000/api/books/?search=Harry
  
  # Order by title (ascending)
  curl http://127.0.0.1:8000/api/books/?ordering=title
  
  # Order by publication year (descending)
  curl http://127.0.0.1:8000/api/books/?ordering=-publication_year
  
  # Combine filters, search, and ordering
  curl "http://127.0.0.1:8000/api/books/?search=Potter&ordering=publication_year"
  ```

#### 2. Retrieve Single Book
- **URL**: `/api/books/<int:pk>/`
- **Method**: `GET`
- **Description**: Retrieve details of a specific book by ID
- **Response**: 200 OK with book object
- **Example**:
  ```bash
  curl http://127.0.0.1:8000/api/books/1/
  ```

### Protected Endpoints (Authentication Required)

#### 3. Create New Book
- **URL**: `/api/books/create/`
- **Method**: `POST`
- **Description**: Create a new book
- **Authentication**: Required (Token)
- **Request Body**:
  ```json
  {
    "title": "Book Title",
    "publication_year": 2024,
    "author": 1
  }
  ```
- **Response**: 201 Created
- **Validation**: `publication_year` cannot be in the future
- **Example**:
  ```bash
  curl -X POST http://127.0.0.1:8000/api/books/create/ \
    -H "Authorization: Token YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"title": "New Book", "publication_year": 2024, "author": 1}'
  ```

#### 4. Update Book
- **URL**: `/api/books/<int:pk>/update/`
- **Methods**: `PUT` (full update), `PATCH` (partial update)
- **Description**: Update an existing book
- **Authentication**: Required (Token)
- **Request Body**: Same as create (PUT requires all fields, PATCH allows partial)
- **Response**: 200 OK
- **Example**:
  ```bash
  curl -X PATCH http://127.0.0.1:8000/api/books/1/update/ \
    -H "Authorization: Token YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"title": "Updated Title"}'
  ```

#### 5. Delete Book
- **URL**: `/api/books/<int:pk>/delete/`
- **Method**: `DELETE`
- **Description**: Delete a book
- **Authentication**: Required (Token)
- **Response**: 204 No Content
- **Example**:
  ```bash
  curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
    -H "Authorization: Token YOUR_TOKEN"
  ```

## Advanced Query Capabilities

The API supports advanced filtering, searching, and ordering features to help you find and organize book data efficiently.

### Filtering

Filter books by specific field values using query parameters.

**Available Filter Fields:**
- `title` - Exact match on book title
- `author__name` - Exact match on author's name
- `publication_year` - Exact match on publication year

**Examples:**
```bash
# Filter by publication year
GET /api/books/?publication_year=1997

# Filter by author name
GET /api/books/?author__name=J.K. Rowling

# Filter by title
GET /api/books/?title=Harry Potter

# Combine multiple filters
GET /api/books/?author__name=J.K. Rowling&publication_year=1997
```

### Searching

Perform text-based searches across multiple fields simultaneously.

**Searchable Fields:**
- `title` - Book title
- `author__name` - Author's name

**Search Parameter:** `?search=<query>`

**Examples:**
```bash
# Search for books containing "Harry" in title or author name
GET /api/books/?search=Harry

# Search for author names containing "Rowling"
GET /api/books/?search=Rowling

# Search is case-insensitive and matches partial text
GET /api/books/?search=potter
```

### Ordering

Sort results by specified fields in ascending or descending order.

**Orderable Fields:**
- `title` - Book title
- `publication_year` - Publication year

**Order Parameter:** `?ordering=<field>` or `?ordering=-<field>` (descending)

**Examples:**
```bash
# Order by title (A-Z)
GET /api/books/?ordering=title

# Order by title (Z-A) - descending
GET /api/books/?ordering=-title

# Order by publication year (oldest first)
GET /api/books/?ordering=publication_year

# Order by publication year (newest first)
GET /api/books/?ordering=-publication_year
```

### Combining Features

You can combine filtering, searching, and ordering in a single request.

**Examples:**
```bash
# Search for "Harry" and order by publication year
GET /api/books/?search=Harry&ordering=publication_year

# Filter by author and order by title
GET /api/books/?author__name=J.K. Rowling&ordering=title

# Filter by year, search for text, and order results
GET /api/books/?publication_year=1997&search=Chamber&ordering=title

# Complex query with all features
GET /api/books/?author__name=J.K. Rowling&search=Potter&ordering=-publication_year
```

### Implementation Details

The filtering, searching, and ordering functionality is implemented using:

1. **django-filter** - Provides `DjangoFilterBackend` for field-based filtering
2. **DRF SearchFilter** - Enables text search across specified fields
3. **DRF OrderingFilter** - Allows result ordering by specified fields

**Configuration in `views.py`:**
```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering
```

**Configuration in `settings.py`:**
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## View Configurations

### Generic Views Used

#### BookListView (ListAPIView)
- **Purpose**: List all books with filtering, searching, and ordering
- **Permission**: `AllowAny` - Public access
- **Features**: 
  - Read-only endpoint
  - Automatic pagination support
  - **Filtering** by title, author__name, publication_year
  - **Searching** across title and author__name fields
  - **Ordering** by title or publication_year
  - Default ordering by title (ascending)
- **Filter Backends**: DjangoFilterBackend, SearchFilter, OrderingFilter

#### BookDetailView (RetrieveAPIView)
- **Purpose**: Retrieve single book
- **Permission**: `AllowAny` - Public access
- **Features**: Read-only, returns 404 if not found

#### BookCreateView (CreateAPIView)
- **Purpose**: Create new books
- **Permission**: `IsAuthenticated` - Requires authentication
- **Custom Behavior**: 
  - Custom `perform_create()` method for additional processing
  - Automatic validation via BookSerializer
  - Returns 201 Created with created object

#### BookUpdateView (UpdateAPIView)
- **Purpose**: Update existing books
- **Permission**: `IsAuthenticated` - Requires authentication
- **Custom Behavior**:
  - Supports both PUT (full) and PATCH (partial) updates
  - Custom `perform_update()` method for additional processing
  - Automatic validation via BookSerializer

#### BookDeleteView (DestroyAPIView)
- **Purpose**: Delete books
- **Permission**: `IsAuthenticated` - Requires authentication
- **Features**: Returns 204 No Content on success

## Serializers

### BookSerializer
- Serializes all Book model fields
- **Custom Validation**: Ensures `publication_year` is not in the future
- **Validation Method**: `validate_publication_year()`

### AuthorSerializer
- Serializes Author with nested books
- **Nested Serialization**: Includes all books by the author
- **Fields**: id, name, books (nested BookSerializer)
- **Read-Only**: books field is read-only

## Authentication

### Token Authentication

1. **Obtain Token**:
   ```bash
   # Create a superuser first
   python manage.py createsuperuser
   
   # Obtain token (if token endpoint is configured)
   curl -X POST http://127.0.0.1:8000/api/api-token-auth/ \
     -d "username=youruser&password=yourpass"
   ```

2. **Use Token in Requests**:
   ```bash
   curl -H "Authorization: Token YOUR_TOKEN_HERE" http://127.0.0.1:8000/api/books/create/
   ```

### Session Authentication
- Enabled for browsable API
- Login via `/admin/` or browsable API interface

## Permissions

### Permission Classes Used

1. **AllowAny** (BookListView, BookDetailView)
   - Public read access
   - No authentication required

2. **IsAuthenticated** (BookCreateView, BookUpdateView, BookDeleteView)
   - Requires valid authentication token
   - Only authenticated users can create, update, or delete

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django djangorestframework
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

### 5. Access API
- Base URL: `http://127.0.0.1:8000/api/`
- Admin: `http://127.0.0.1:8000/admin/`

## Testing

### Manual Testing with cURL

#### Test Public Access (No Auth)
```bash
# Should work - List books
curl http://127.0.0.1:8000/api/books/

# Should work - Get single book
curl http://127.0.0.1:8000/api/books/1/

# Should fail - Create book without auth
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "publication_year": 2024, "author": 1}'
```

#### Test Authenticated Access
```bash
# First, obtain your token or create one in Django admin

# Create book with auth - Should work
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Authenticated Book", "publication_year": 2024, "author": 1}'

# Update book with auth - Should work
curl -X PATCH http://127.0.0.1:8000/api/books/1/update/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'

# Delete book with auth - Should work
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Test Validation
```bash
# Should fail - Future publication year
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Future Book", "publication_year": 2030, "author": 1}'
```

#### Test Filtering, Searching, and Ordering
```bash
# Test filtering by publication year
curl "http://127.0.0.1:8000/api/books/?publication_year=1997"

# Test filtering by author
curl "http://127.0.0.1:8000/api/books/?author__name=J.K. Rowling"

# Test search functionality
curl "http://127.0.0.1:8000/api/books/?search=Harry"

# Test ordering (ascending)
curl "http://127.0.0.1:8000/api/books/?ordering=title"

# Test ordering (descending)
curl "http://127.0.0.1:8000/api/books/?ordering=-publication_year"

# Test combined filtering and searching
curl "http://127.0.0.1:8000/api/books/?search=Potter&publication_year=1997"

# Test all features together
curl "http://127.0.0.1:8000/api/books/?author__name=J.K. Rowling&search=Chamber&ordering=publication_year"
```

### Using Postman

1. **Set Base URL**: `http://127.0.0.1:8000`
2. **For Protected Endpoints**:
   - Go to Authorization tab
   - Select Type: "API Key"
   - Key: "Authorization"
   - Value: "Token YOUR_TOKEN"
   - Add to: Header

## Project Structure

```
advanced-api-project/
├── advanced_api_project/
│   ├── settings.py          # Project settings with REST_FRAMEWORK config
│   ├── urls.py              # Main URL configuration
│   └── ...
├── api/
│   ├── models.py            # Author and Book models
│   ├── serializers.py       # BookSerializer and AuthorSerializer
│   ├── views.py             # Generic views for CRUD operations
│   ├── urls.py              # API endpoint routing
│   ├── admin.py             # Admin configuration
│   └── migrations/
├── manage.py
├── db.sqlite3
└── README.md
```

## Key Features Implemented

✅ **Custom Serializers**
- BookSerializer with custom validation
- AuthorSerializer with nested relationships

✅ **Generic Views**
- ListAPIView for listing books
- RetrieveAPIView for retrieving single book
- CreateAPIView for creating books
- UpdateAPIView for updating books (PUT/PATCH)
- DestroyAPIView for deleting books

✅ **Authentication**
- Token authentication
- Session authentication for browsable API

✅ **Permissions**
- Public read access for lists and details
- Authenticated-only access for create, update, delete

✅ **Advanced Query Capabilities**
- **Filtering** by title, author name, and publication year
- **Searching** across title and author name fields
- **Ordering** by title or publication year (ascending/descending)
- Support for combining multiple query parameters

✅ **Custom Behavior**
- `perform_create()` hook in CreateView
- `perform_update()` hook in UpdateView
- Custom validation in serializers

✅ **Documentation**
- Comprehensive docstrings in views
- Detailed comments in code
- Complete API documentation in README with examples

## Configuration Details

### settings.py - REST Framework Configuration
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

### Custom Hooks in Views

**perform_create() in BookCreateView**:
- Called before saving a new instance
- Allows modification of save behavior
- Can add additional fields or processing

**perform_update() in BookUpdateView**:
- Called before updating an instance
- Allows modification of update behavior
- Can track changes or add metadata

## Troubleshooting

### 401 Unauthorized
- Ensure you're including the token in the Authorization header
- Format: `Authorization: Token YOUR_TOKEN`
- Verify token is valid in Django admin

### 403 Forbidden
- Check if the user has the required permissions
- Ensure you're using the correct HTTP method

### 400 Bad Request
- Check request body format (must be valid JSON)
- Verify all required fields are included
- Check validation rules (e.g., publication_year not in future)

### 404 Not Found
- Verify the book ID exists
- Check the URL pattern is correct

## Testing

### Test Suite Overview

The project includes comprehensive unit tests covering all API endpoints and functionalities. The test suite includes 43 tests organized into the following categories:

#### Test Categories

1. **CRUD Operations Tests**
   - Book creation with authentication
   - Book retrieval (list and detail views)
   - Book updates (full and partial)
   - Book deletion
   - Validation testing (e.g., future publication year)

2. **Filtering Tests**
   - Filter by title
   - Filter by author name  
   - Filter by publication year
   - Multiple filter combinations
   - No results scenarios

3. **Searching Tests**
   - Search by title
   - Search by author name
   - Case-insensitive searching
   - Partial text matching
   - No results scenarios

4. **Ordering Tests**
   - Order by title (ascending/descending)
   - Order by publication year (ascending/descending)
   - Default ordering verification

5. **Combined Query Tests**
   - Filter + Search
   - Filter + Ordering
   - Search + Ordering
   - Filter + Search + Ordering

6. **Authentication & Permission Tests**
   - Public access for read operations
   - Authentication requirements for write operations
   - Token-based authentication
   - Unauthorized access attempts

### Running Tests

Execute the full test suite:
```bash
cd advanced-api-project
python manage.py test api
```

Run specific test classes:
```bash
# Test only CRUD operations
python manage.py test api.test_views.BookCreateViewTests

# Test only filtering
python manage.py test api.test_views.BookFilteringTests

# Test only search functionality
python manage.py test api.test_views.BookSearchTests

# Test only ordering
python manage.py test api.test_views.BookOrderingTests

# Test only permissions
python manage.py test api.test_views.PermissionTests
```

Run specific test methods:
```bash
python manage.py test api.test_views.BookCreateViewTests.test_create_book_authenticated
```

### Test Output

Successful test run output:
```
Found 43 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........................................
----------------------------------------------------------------------
Ran 43 tests in X.XXXs

OK
Destroying test database for alias 'default'...
```

### Test Coverage

The test suite covers:
- ✅ All 5 API endpoints (List, Detail, Create, Update, Delete)
- ✅ Authentication and permission enforcement
- ✅ Data validation (custom and built-in)
- ✅ Filtering by all configured fields
- ✅ Search functionality across multiple fields
- ✅ Ordering in both directions
- ✅ Combined query operations
- ✅ Error handling and edge cases
- ✅ HTTP status codes verification
- ✅ Response data integrity

### Testing Best Practices

The test suite follows Django testing best practices:
- Uses separate test database (automatically created and destroyed)
- Each test is independent and isolated
- setUp() method creates fresh test data for each test
- Descriptive test names explaining what is being tested
- Tests both positive and negative scenarios
- Comprehensive docstrings for all test classes and methods

### Continuous Integration

To integrate tests into CI/CD pipeline:
```yaml
# Example for GitHub Actions
- name: Run Tests
  run: |
    python manage.py test api
```

## Future Enhancements

Potential improvements:
- Add pagination customization
- Create custom permission classes
- Add throttling for rate limiting
- Implement versioning
- Add more complex filtering options
- Implement caching strategies
- Add performance testing

## License

This project is for educational purposes as part of the ALX Django Learning Lab.
