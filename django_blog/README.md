# Django Blog Project

A comprehensive Django blog application with user authentication, post management, and a responsive design.

## Project Overview

This Django blog project provides a complete blogging platform with the following features:
- **User Authentication System**: Registration, login, logout, and profile management
- User-generated blog posts
- Post management through Django admin
- Responsive design with modern CSS
- SQLite database for development
- Static files and template management
- Secure CSRF protection on all forms

## Documentation

- **[Authentication System Documentation](AUTHENTICATION_DOCUMENTATION.md)** - Comprehensive guide to the user authentication system
- **Main README** (this file) - Project overview and setup instructions

## Project Structure

```
django_blog/
├── manage.py
├── db.sqlite3
├── AUTHENTICATION_DOCUMENTATION.md  # Auth system docs
├── django_blog/              # Project configuration
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
└── blog/                     # Blog application
    ├── __init__.py
    ├── admin.py              # Admin configuration
    ├── apps.py
    ├── forms.py              # Authentication forms
    ├── models.py             # Post model
    ├── views.py              # View functions (auth + blog)
    ├── urls.py               # Blog URL patterns
    ├── tests.py
    ├── migrations/           # Database migrations
    │   └── 0001_initial.py
    ├── templates/            # HTML templates
    │   └── blog/
    │       ├── base.html     # Base template
    │       ├── home.html     # Home page
    │       ├── login.html    # Login page
    │       ├── register.html # Registration page
    │       ├── logout.html   # Logout confirmation
    │       └── profile.html  # User profile
    └── static/               # Static files
        └── blog/
            ├── css/
            │   └── style.css # Stylesheet (with auth styles)
            └── js/
                └── main.js   # JavaScript
```

## Models

### Post Model
The `Post` model represents a blog post with the following fields:

- `title`: CharField(max_length=200) - The post title
- `content`: TextField - The main content of the post
- `published_date`: DateTimeField(auto_now_add=True) - Auto-set on creation
- `author`: ForeignKey(User) - Links to Django's User model

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Install Django**:
   ```bash
   pip install django
   ```

2. **Navigate to the project directory**:
   ```bash
   cd django_blog
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations blog
   python manage.py migrate
   ```

4. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Login: http://127.0.0.1:8000/login/
   - Register: http://127.0.0.1:8000/register/
   - Profile: http://127.0.0.1:8000/profile/ (requires login)

## Quick Start Guide

### Register a New Account
1. Go to http://127.0.0.1:8000/register/
2. Fill in username, email, and password
3. Click "Register"
4. You'll be automatically logged in

### Login to Existing Account
1. Go to http://127.0.0.1:8000/login/
2. Enter your username and password
3. Click "Login"

### Manage Your Profile
1. After logging in, click "Profile" in the navigation
2. View your account information
3. Edit your username or email
4. Click "Update Profile" to save changes

## Configuration

### Database
The project uses SQLite by default, configured in `django_blog/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
```

To use PostgreSQL or another database, modify the `DATABASES` setting accordingly.

### Static Files
Static files are configured in `settings.py`:

```python
STATIC_URL = 'static/'
```

Static files are organized under `blog/static/blog/` directory.

### Templates
Templates are stored in `blog/templates/blog/` directory. Django automatically discovers these templates because `APP_DIRS` is set to `True` in the `TEMPLATES` setting.

## Usage

### Creating Blog Posts

1. Access the admin panel at http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Click on "Posts" under the BLOG section
4. Click "Add Post" to create a new blog post
5. Fill in the title, content, and select an author
6. Click "Save" to publish the post

### Viewing Blog Posts

Visit http://127.0.0.1:8000/ to see all published blog posts on the home page.

## Features

### Current Features
- ✅ **User Authentication System**:
  - User registration with email
  - Login/logout functionality
  - Profile management (view and edit)
  - Secure password hashing
  - CSRF protection
  - Session management
- ✅ Post model with title, content, publication date, and author
- ✅ Admin interface for managing posts
- ✅ Responsive home page displaying all posts
- ✅ Clean, modern design with CSS styling
- ✅ Message framework integration
- ✅ Static file management
- ✅ Protected routes with login required

### Planned Features
- Post detail pages
- Post creation, editing, and deletion from the frontend
- Comments system
- Post categories and tags
- Search functionality
- Pagination
- Email verification
- Password reset functionality

## Development

### Running Tests
```bash
python manage.py test blog
```

### Making Model Changes
1. Modify `blog/models.py`
2. Create migrations: `python manage.py makemigrations blog`
3. Apply migrations: `python manage.py migrate`

### Collecting Static Files (for production)
```bash
python manage.py collectstatic
```

## Technologies Used

- **Django 5.2.7**: Web framework
- **SQLite**: Database (development)
- **HTML5**: Markup
- **CSS3**: Styling
- **JavaScript**: Client-side interactivity

## Admin Configuration

The Post model is registered with the Django admin with the following features:
- List display: title, author, published_date
- List filters: published_date, author
- Search fields: title, content
- Date hierarchy: published_date

## Security Notes

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS` properly
3. Use environment variables for sensitive data
4. Use a production-grade database (PostgreSQL, MySQL)
5. Configure HTTPS
6. Set up proper static file serving

## Contributing

This is a learning project. Feel free to extend it with additional features like:
- User authentication system
- Post categories and tags
- Comment functionality
- Rich text editor integration
- Image upload for posts
- RSS feed

## License

This project is created for educational purposes as part of the ALX Django Learning Lab.

## Repository

- **GitHub Repository**: Alx_DjangoLearnLab
- **Directory**: django_blog

## Author

Created as part of the ALX Django Learning Lab curriculum.
