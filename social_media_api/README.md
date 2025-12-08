# Social Media API

A Django REST Framework-based API for a social media application with user authentication, profiles, posts, comments, and follower functionality.

## Project Overview

This project provides the foundational backend for a social media platform, including:
- Custom user model with extended profile fields
- Token-based authentication
- User registration and login endpoints
- Profile management
- Posts with full CRUD operations
- Comments on posts
- Pagination and filtering

## Setup Instructions

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/skaduteye/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/social_media_api
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework django-filter
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/accounts/register/` | POST | Register a new user | None |
| `/api/accounts/login/` | POST | Login and get token | None |
| `/api/accounts/profile/` | GET | Get current user profile | Token required |
| `/api/accounts/profile/` | PUT/PATCH | Update user profile | Token required |
| `/api/accounts/users/` | GET | List all users | Token required |

### Follow Management Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/accounts/follow/<user_id>/` | POST | Follow a user | Token required |
| `/api/accounts/unfollow/<user_id>/` | POST | Unfollow a user | Token required |

### Feed Endpoint

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/feed/` | GET | Get posts from followed users | Token required |

### Posts Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/posts/` | GET | List all posts (paginated) | Token required |
| `/api/posts/` | POST | Create a new post | Token required |
| `/api/posts/{id}/` | GET | Get a specific post | Token required |
| `/api/posts/{id}/` | PUT | Update a post (owner only) | Token required |
| `/api/posts/{id}/` | PATCH | Partial update a post | Token required |
| `/api/posts/{id}/` | DELETE | Delete a post (owner only) | Token required |

### Comments Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/comments/` | GET | List all comments (paginated) | Token required |
| `/api/comments/` | POST | Create a new comment | Token required |
| `/api/comments/{id}/` | GET | Get a specific comment | Token required |
| `/api/comments/{id}/` | PUT | Update a comment (owner only) | Token required |
| `/api/comments/{id}/` | PATCH | Partial update a comment | Token required |
| `/api/comments/{id}/` | DELETE | Delete a comment (owner only) | Token required |

### Likes Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/posts/{id}/like/` | POST | Like a post | Token required |
| `/api/posts/{id}/unlike/` | POST | Unlike a post | Token required |

### Notifications Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/notifications/` | GET | List all notifications | Token required |
| `/api/notifications/{id}/` | GET | Get a specific notification | Token required |
| `/api/notifications/{id}/read/` | POST | Mark a notification as read | Token required |
| `/api/notifications/mark-all-read/` | POST | Mark all notifications as read | Token required |
| `/api/notifications/unread-count/` | GET | Get unread notification count | Token required |

### User Registration

**Endpoint:** `POST /api/accounts/register/`

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "bio": "Hello, I'm John!"
}
```

**Response (201 Created):**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "bio": "Hello, I'm John!",
        "profile_picture": null,
        "followers": [],
        "following": [],
        "date_joined": "2025-12-08T12:00:00Z"
    },
    "token": "your-auth-token-here",
    "message": "User registered successfully."
}
```

### User Login

**Endpoint:** `POST /api/accounts/login/`

**Request Body:**
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "bio": "Hello, I'm John!",
        "profile_picture": null,
        "followers": [],
        "following": [],
        "date_joined": "2025-12-08T12:00:00Z"
    },
    "token": "your-auth-token-here",
    "message": "Login successful."
}
```

### User Profile

**Endpoint:** `GET /api/accounts/profile/`

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Hello, I'm John!",
    "profile_picture": null,
    "followers_count": 5,
    "following_count": 10,
    "date_joined": "2025-12-08T12:00:00Z"
}
```

### Follow Management

#### Follow a User

**Endpoint:** `POST /api/accounts/follow/<user_id>/`

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Response (200 OK):**
```json
{
    "message": "You are now following janedoe.",
    "following": "janedoe"
}
```

**Error Response (400 Bad Request):**
```json
{
    "error": "You cannot follow yourself."
}
```

#### Unfollow a User

**Endpoint:** `POST /api/accounts/unfollow/<user_id>/`

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Response (200 OK):**
```json
{
    "message": "You have unfollowed janedoe.",
    "unfollowed": "janedoe"
}
```

### Feed

#### Get Your Feed

**Endpoint:** `GET /api/feed/`

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Description:** Returns posts from users you follow, ordered by most recent first.

**Response (200 OK):**
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/feed/?page=2",
    "previous": null,
    "results": [
        {
            "id": 5,
            "author": "janedoe",
            "author_id": 2,
            "title": "Latest Post from Jane",
            "content": "This is my latest update!",
            "created_at": "2025-12-08T14:00:00Z",
            "updated_at": "2025-12-08T14:00:00Z",
            "comments_count": 3
        },
        {
            "id": 3,
            "author": "bobsmith",
            "author_id": 3,
            "title": "Bob's Post",
            "content": "Hello everyone!",
            "created_at": "2025-12-08T12:00:00Z",
            "updated_at": "2025-12-08T12:00:00Z",
            "comments_count": 1
        }
    ]
}
```

### Posts

#### Create a Post

**Endpoint:** `POST /api/posts/`

**Headers:**
```
Authorization: Token your-auth-token-here
Content-Type: application/json
```

**Request Body:**
```json
{
    "title": "My First Post",
    "content": "This is the content of my first post on the platform!"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "author": "johndoe",
    "author_id": 1,
    "title": "My First Post",
    "content": "This is the content of my first post on the platform!",
    "created_at": "2025-12-08T12:00:00Z",
    "updated_at": "2025-12-08T12:00:00Z",
    "comments": [],
    "comments_count": 0
}
```

#### List Posts with Filtering

**Endpoint:** `GET /api/posts/`

**Query Parameters:**
- `search` - Search in title and content (e.g., `?search=django`)
- `author` - Filter by author ID (e.g., `?author=1`)
- `ordering` - Order results (e.g., `?ordering=-created_at`)
- `page` - Page number for pagination (e.g., `?page=2`)

**Example:** `GET /api/posts/?search=python&ordering=-created_at`

### Comments

#### Create a Comment

**Endpoint:** `POST /api/comments/`

**Headers:**
```
Authorization: Token your-auth-token-here
Content-Type: application/json
```

**Request Body:**
```json
{
    "post": 1,
    "content": "Great post! Thanks for sharing."
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "post": 1,
    "author": "janedoe",
    "author_id": 2,
    "content": "Great post! Thanks for sharing.",
    "created_at": "2025-12-08T12:05:00Z",
    "updated_at": "2025-12-08T12:05:00Z"
}
```

#### Filter Comments by Post

**Endpoint:** `GET /api/comments/?post=1`

## User Model

The custom `CustomUser` model extends Django's `AbstractUser` and includes the following additional fields:

| Field | Type | Description |
|-------|------|-------------|
| `bio` | TextField | A short biography (max 500 characters) |
| `profile_picture` | ImageField | Profile image upload |
| `followers` | ManyToManyField (self) | Users who follow this user |
| `following` | ManyToManyField (self) | Users this user follows (reverse relation) |

### Followers Relationship

The `followers` field is a self-referential ManyToMany field with `symmetrical=False`, meaning:
- If User A follows User B, User B doesn't automatically follow User A
- `user.followers.all()` - Get all users following this user
- `user.following.all()` - Get all users this user follows

## Authentication

This API uses **Token Authentication** provided by Django REST Framework.

### How to Use Tokens

1. **Register** a new user or **login** to get your authentication token
2. Include the token in the `Authorization` header for protected endpoints:
   ```
   Authorization: Token your-auth-token-here
   ```

## Project Structure

```
social_media_api/
├── manage.py
├── db.sqlite3
├── README.md
├── social_media_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # CustomUser model
│   ├── serializers.py     # User serializers
│   ├── views.py           # Auth views
│   ├── urls.py            # URL routing
│   ├── tests.py
│   └── migrations/
└── posts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py          # Post and Comment models
    ├── serializers.py     # Post and Comment serializers
    ├── views.py           # ViewSets for CRUD operations
    ├── urls.py            # Router-based URL routing
    ├── tests.py
    └── migrations/
```

## Pagination

All list endpoints are paginated with a default page size of 10 items per page.

**Response Format:**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [...]
}
```

## Filtering and Search

### Posts
- **Search:** `?search=keyword` - Searches in title and content
- **Filter by author:** `?author=1`
- **Ordering:** `?ordering=-created_at` (prefix with `-` for descending)
  - Available fields: `created_at`, `updated_at`, `title`

### Comments
- **Filter by post:** `?post=1`
- **Filter by author:** `?author=1`
- **Ordering:** `?ordering=created_at`

## Permissions

- **Read operations** (GET): Available to all authenticated users
- **Create operations** (POST): Available to all authenticated users
- **Update/Delete operations** (PUT, PATCH, DELETE): Only available to the content owner

## Testing with Postman

1. **Register a user:**
   - Method: POST
   - URL: `http://localhost:8000/api/accounts/register/`
   - Body (JSON): Include username, email, password, password2

2. **Login:**
   - Method: POST
   - URL: `http://localhost:8000/api/accounts/login/`
   - Body (JSON): Include username, password
   - Copy the token from the response

3. **Access protected endpoints:**
   - Add header: `Authorization: Token <your-token>`

4. **Create a post:**
   - Method: POST
   - URL: `http://localhost:8000/api/posts/`
   - Headers: `Authorization: Token <your-token>`
   - Body (JSON): Include title, content

5. **Add a comment:**
   - Method: POST
   - URL: `http://localhost:8000/api/comments/`
   - Headers: `Authorization: Token <your-token>`
   - Body (JSON): Include post (ID), content

6. **Search posts:**
   - Method: GET
   - URL: `http://localhost:8000/api/posts/?search=keyword`

## Technologies Used

- **Django 5.2.7** - Web framework
- **Django REST Framework** - API toolkit
- **django-filter** - Filtering support
- **SQLite** - Database (development)
- **Token Authentication** - API security

## License

This project is for educational purposes as part of the ALX Django LearnLab curriculum.
