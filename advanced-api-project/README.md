# Advanced API Project - Django REST Framework

A comprehensive Django REST Framework project demonstrating custom views, generic views, nested serializers, and authentication/permissions.

## Project Overview

This project provides a RESTful API for managing books and authors with the following features:
- Custom serializers with nested relationships
- Generic views for CRUD operations
- Token-based authentication
- Role-based permissions
- Custom validation

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
- **Description**: Retrieve a list of all books
- **Response**: 200 OK with array of book objects
- **Example**:
  ```bash
  curl http://127.0.0.1:8000/api/books/
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

## View Configurations

### Generic Views Used

#### BookListView (ListAPIView)
- **Purpose**: List all books
- **Permission**: `AllowAny` - Public access
- **Features**: Read-only, automatic pagination support

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

✅ **Custom Behavior**
- `perform_create()` hook in CreateView
- `perform_update()` hook in UpdateView
- Custom validation in serializers

✅ **Documentation**
- Comprehensive docstrings in views
- Detailed comments in code
- Complete API documentation in README

## Configuration Details

### settings.py - REST Framework Configuration
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
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

## Future Enhancements

Potential improvements:
- Add filtering and search capabilities
- Implement pagination customization
- Add ordering/sorting options
- Create custom permission classes
- Add throttling for rate limiting
- Implement versioning
- Add more complex filtering with django-filter

## License

This project is for educational purposes as part of the ALX Django Learning Lab.
