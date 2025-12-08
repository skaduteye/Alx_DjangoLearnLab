# Social Media API

A Django REST Framework-based API for a social media application with user authentication, profiles, and follower functionality.

## Project Overview

This project provides the foundational backend for a social media platform, including:
- Custom user model with extended profile fields
- Token-based authentication
- User registration and login endpoints
- Profile management

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
   pip install django djangorestframework
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
└── accounts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py          # CustomUser model
    ├── serializers.py     # API serializers
    ├── views.py           # API views
    ├── urls.py            # URL routing
    ├── tests.py
    └── migrations/
        └── 0001_initial.py
```

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

## Technologies Used

- **Django 5.2.7** - Web framework
- **Django REST Framework** - API toolkit
- **SQLite** - Database (development)
- **Token Authentication** - API security

## License

This project is for educational purposes as part of the ALX Django LearnLab curriculum.
