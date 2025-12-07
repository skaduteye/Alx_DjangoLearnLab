# Django Blog Project

A comprehensive Django blog application with user authentication, post management, and a responsive design.

## Project Overview

This Django blog project provides a complete blogging platform with the following features:
- **User Authentication System**: Registration, login, logout, and profile management
- **Blog Post Management**: Full CRUD operations for blog posts
- **Comment System**: Interactive commenting on blog posts
- **Class-Based Views**: Efficient Django CBV implementation
- **Permission Controls**: Author-only edit/delete functionality
- **Responsive Design**: Modern CSS with grid layouts
- **Pagination**: Automatic post pagination
- SQLite database for development
- Static files and template management
- Secure CSRF protection on all forms

## Documentation

- **[Comment Functionality Documentation](COMMENT_FUNCTIONALITY.md)** - Complete guide to the comment system
- **[Blog Post Management Documentation](BLOG_POST_MANAGEMENT.md)** - Complete guide to post CRUD operations
- **[Authentication System Documentation](AUTHENTICATION_DOCUMENTATION.md)** - Comprehensive guide to the user authentication system
- **Main README** (this file) - Project overview and setup instructions

## Project Structure

```
django_blog/
├── manage.py
├── db.sqlite3
├── COMMENT_FUNCTIONALITY.md  # Comment system docs
├── BLOG_POST_MANAGEMENT.md   # Blog post CRUD docs
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
    ├── forms.py              # Authentication, post & comment forms
    ├── models.py             # Post & Comment models
    ├── views.py              # CBV and function views
    ├── urls.py               # Blog URL patterns
    ├── tests.py
    ├── migrations/           # Database migrations
    │   ├── 0001_initial.py
    │   └── 0002_comment.py
    ├── templates/            # HTML templates
    │   └── blog/
            ├── base.html     # Base template
            ├── home.html     # Home page
            ├── post_list.html    # All posts list
            ├── post_detail.html  # Single post view (with comments)
            ├── post_form.html    # Create/Edit post form
            ├── post_confirm_delete.html  # Delete post confirmation
            ├── comment_form.html # Create/Edit comment form
            ├── comment_confirm_delete.html  # Delete comment confirmation
            ├── login.html    # Login page
            ├── register.html # Registration page
            ├── logout.html   # Logout confirmation
            └── profile.html  # User profile
    └── static/               # Static files
        └── blog/
            ├── css/
            │   └── style.css # Stylesheet (with comment styles)
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

### Comment Model
The `Comment` model represents comments on blog posts with the following fields:

- `post`: ForeignKey(Post) - Links to the Post being commented on
- `author`: ForeignKey(User) - The user who wrote the comment
- `content`: TextField - The comment text
- `created_at`: DateTimeField(auto_now_add=True) - Auto-set on creation
- `updated_at`: DateTimeField(auto_now=True) - Auto-updated on modification

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

### Managing Blog Posts (Frontend)

#### Viewing Posts
- **All Posts**: Visit http://127.0.0.1:8000/posts/
- **Single Post**: Click on any post title or "Read More" button
- **Home Page**: Visit http://127.0.0.1:8000/ for the welcome page

#### Creating a Post
1. Log in to your account
2. Click "New Post" in the navigation menu
3. Fill in the post title and content
4. Click "Publish Post"
5. Your post will be published immediately

#### Editing a Post
1. Navigate to your post
2. Click "Edit Post" button (only visible if you're the author)
3. Modify title and/or content
4. Click "Update Post"

#### Deleting a Post
1. Navigate to your post
2. Click "Delete Post" button (only visible if you're the author)
3. Confirm deletion on the confirmation page

### Managing Comments (Frontend)

#### Viewing Comments
- Comments are displayed below each blog post
- All users can view comments without logging in
- Comment count is shown in the post detail sidebar

#### Adding a Comment
1. **Must be logged in** (login prompt shown if not authenticated)
2. Navigate to any blog post detail page
3. Scroll to the "Comments" section
4. Type your comment in the textarea (minimum 3 characters)
5. Click "Post Comment"
6. Your comment appears immediately with your username and timestamp

#### Editing Your Comment
1. Find your comment in the comments list
2. Click the "Edit" button (only visible on your own comments)
3. Modify the comment text
4. Click "Update Comment"
5. Comment shows an "(edited)" badge with the updated content

#### Deleting Your Comment
1. Find your comment in the comments list
2. Click the "Delete" button (only visible on your own comments)
3. Review the comment preview on the confirmation page
4. Click "Yes, Delete Comment" to permanently remove it
5. You'll be redirected back to the post

### Managing Blog Posts (Admin Panel)

1. Access the admin panel at http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Click on "Posts" under the BLOG section
4. Add, edit, or delete posts through the admin interface

### Managing Comments (Admin Panel)

1. Access the admin panel at http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Click on "Comments" under the BLOG section
4. View, edit, or delete comments
5. Filter by date, author, or search by content

## Features

### Current Features
- ✅ **Blog Post Management (CRUD)**:
  - Create new blog posts (authenticated users)
  - View all posts in paginated list
  - View individual post details
  - Edit your own posts (authors only)
  - Delete your own posts (authors only)
  - Automatic author attribution
  - Pagination (10 posts per page)
  - Responsive grid layout

- ✅ **Comment System**:
  - View comments on all posts
  - Add comments (authenticated users)
  - Edit your own comments (authors only)
  - Delete your own comments (authors only)
  - Inline comment form on post detail page
  - Comment metadata (author, timestamp, edited badge)
  - Comment count display
  - Minimum 3 character validation
  - Permission controls for comment management

- ✅ **User Authentication System**:
  - User registration with email
  - Login/logout functionality
  - Profile management (view and edit)
  - Secure password hashing
  - CSRF protection
  - Session management

- ✅ **Technical Features**:
  - Class-based views (ListView, DetailView, CreateView, UpdateView, DeleteView)
  - Permission controls (LoginRequiredMixin, UserPassesTestMixin)
  - Post model with title, content, publication date, and author
  - Comment model with content, timestamps, and relationships
  - Admin interface for managing posts and comments
  - Responsive design with modern CSS
  - Message framework integration
  - Static file management
  - Protected routes with login required

### Planned Features
- Nested comment replies (threading)
- Post categories and tags
- Search functionality
- Rich text editor for posts and comments
- Email verification
- Password reset functionality
- Featured images for posts
- Post analytics (views, likes)
- Social sharing
- Comment pagination
- Comment likes/voting

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
