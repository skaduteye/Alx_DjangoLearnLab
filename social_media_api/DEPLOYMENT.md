# Deployment Guide for Social Media API

This document provides comprehensive instructions for deploying the Social Media API to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Production Configuration](#production-configuration)
3. [Deployment to Heroku](#deployment-to-heroku)
4. [Alternative Deployment Options](#alternative-deployment-options)
5. [Environment Variables](#environment-variables)
6. [Database Setup](#database-setup)
7. [Static Files](#static-files)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Security Considerations](#security-considerations)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- Python 3.13+ installed locally
- Git installed and configured
- A GitHub account with the repository pushed
- A Heroku account (or alternative hosting service)
- Heroku CLI installed (for Heroku deployment)

## Production Configuration

The application has been configured for production with the following settings:

### Security Settings (when DEBUG=False)

| Setting | Value | Description |
|---------|-------|-------------|
| `SECURE_SSL_REDIRECT` | True | Redirects all HTTP to HTTPS |
| `SESSION_COOKIE_SECURE` | True | Session cookies only sent over HTTPS |
| `CSRF_COOKIE_SECURE` | True | CSRF cookies only sent over HTTPS |
| `SECURE_HSTS_SECONDS` | 31536000 | HTTP Strict Transport Security (1 year) |
| `SECURE_BROWSER_XSS_FILTER` | True | Browser XSS filtering enabled |
| `X_FRAME_OPTIONS` | DENY | Prevent clickjacking attacks |
| `SECURE_CONTENT_TYPE_NOSNIFF` | True | Prevent MIME type sniffing |

### Configuration Files

| File | Purpose |
|------|---------|
| `Procfile` | Heroku process configuration |
| `runtime.txt` | Python version specification |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variables template |

---

## Deployment to Heroku

### Step 1: Install Heroku CLI

```bash
# Windows (using Chocolatey)
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login to Heroku

```bash
heroku login
```

### Step 3: Create a Heroku App

```bash
cd social_media_api
heroku create your-app-name
```

### Step 4: Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:essential-0
```

### Step 5: Configure Environment Variables

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set environment variables
heroku config:set SECRET_KEY='your-generated-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'
heroku config:set DJANGO_LOG_LEVEL=INFO
```

### Step 6: Deploy the Application

```bash
git push heroku master
```

### Step 7: Run Migrations

```bash
heroku run python manage.py migrate
```

### Step 8: Create Superuser (Optional)

```bash
heroku run python manage.py createsuperuser
```

### Step 9: Collect Static Files

```bash
heroku run python manage.py collectstatic --noinput
```

### Step 10: Open the Application

```bash
heroku open
```

---

## Alternative Deployment Options

### AWS Elastic Beanstalk

1. Install AWS CLI and EB CLI
2. Configure AWS credentials
3. Create `.ebextensions/django.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: social_media_api.wsgi:application
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: staticfiles
```

4. Deploy:
```bash
eb init -p python-3.13 social-media-api
eb create social-media-api-env
eb deploy
```

### DigitalOcean App Platform

1. Connect your GitHub repository
2. Configure environment variables in the dashboard
3. Set the run command: `gunicorn social_media_api.wsgi:application`
4. Deploy

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_media_api.wsgi:application"]
```

---

## Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `SECRET_KEY` | Yes | Django secret key | Development key |
| `DEBUG` | No | Debug mode | False |
| `ALLOWED_HOSTS` | Yes | Comma-separated hosts | localhost,127.0.0.1 |
| `DATABASE_URL` | No | Database connection URL | SQLite |
| `DJANGO_LOG_LEVEL` | No | Logging level | INFO |

### Generating a Secret Key

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Database Setup

### PostgreSQL (Recommended for Production)

1. Create a PostgreSQL database
2. Set the `DATABASE_URL` environment variable:

```
DATABASE_URL=postgres://username:password@host:5432/database_name
```

### Database Migrations

Always run migrations after deployment:

```bash
python manage.py migrate
```

---

## Static Files

Static files are managed using WhiteNoise middleware.

### Configuration

- `STATIC_URL`: `/static/`
- `STATIC_ROOT`: `BASE_DIR / 'staticfiles'`
- `STATICFILES_STORAGE`: `whitenoise.storage.CompressedManifestStaticFilesStorage`

### Collecting Static Files

```bash
python manage.py collectstatic --noinput
```

---

## Monitoring and Maintenance

### Heroku Logs

```bash
# View logs
heroku logs --tail

# View specific log type
heroku logs --source app --tail
```

### Health Checks

Monitor the following endpoints:

| Endpoint | Expected Response |
|----------|-------------------|
| `/api/` | API root (requires auth) |
| `/admin/` | Django admin login page |

### Regular Maintenance Tasks

1. **Weekly**:
   - Review application logs for errors
   - Check database performance

2. **Monthly**:
   - Update dependencies (`pip install --upgrade`)
   - Review security advisories
   - Backup database

3. **Quarterly**:
   - Rotate secret keys
   - Review and update API documentation
   - Performance optimization review

### Dependency Updates

```bash
# Check for outdated packages
pip list --outdated

# Update requirements
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

---

## Security Considerations

### Production Checklist

- [ ] `DEBUG` is set to `False`
- [ ] `SECRET_KEY` is a secure, random value
- [ ] `ALLOWED_HOSTS` is properly configured
- [ ] HTTPS is enforced (`SECURE_SSL_REDIRECT`)
- [ ] Security headers are enabled
- [ ] Database credentials are secured
- [ ] Admin panel is protected

### Security Headers

The application automatically sets these headers in production:

- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`

---

## Troubleshooting

### Common Issues

#### 1. Static Files Not Loading

```bash
heroku run python manage.py collectstatic --noinput
```

#### 2. Database Connection Errors

Verify `DATABASE_URL` is set correctly:
```bash
heroku config:get DATABASE_URL
```

#### 3. Application Crashes

Check logs for errors:
```bash
heroku logs --tail
```

#### 4. Migration Errors

```bash
heroku run python manage.py migrate --verbosity 2
```

#### 5. Memory Issues

Monitor dyno metrics:
```bash
heroku ps
heroku metrics
```

### Getting Help

- Django Documentation: https://docs.djangoproject.com/
- Heroku Django Guide: https://devcenter.heroku.com/articles/django-app-configuration
- Django REST Framework: https://www.django-rest-framework.org/

---

## Live Application

**Production URL**: `https://your-app-name.herokuapp.com`

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/accounts/register/` | User registration |
| `/api/accounts/login/` | User login |
| `/api/posts/` | Posts CRUD |
| `/api/posts/{id}/like/` | Like a post |
| `/api/posts/{id}/unlike/` | Unlike a post |
| `/api/notifications/` | User notifications |
| `/api/feed/` | User feed |

---

## Changelog

### Version 1.0.0
- Initial production deployment configuration
- Heroku deployment support
- WhiteNoise static file serving
- PostgreSQL database support
- Security hardening for production
