# Mini Blog Backend API

A production-ready Django REST API for a mini blog system with user authentication, public/private posts, commenting, and Celery-based email notifications.

## 🚀 Features

- **User Authentication**
  - Email-based signup with verification
  - JWT-based login (Access + Refresh tokens)
  - Email verification with signed tokens (24-hour expiry)
  - Verified-users-only access

- **Post Management**
  - Create public and private posts
  - List posts with visibility filters
  - Full CRUD operations with ownership checks
  - Private posts visible only to author

- **Comment System**
  - Comment on public posts only
  - Async email notifications to post authors via Celery
  - Delete own comments only
  - Owner and permission validation

- **Email Notifications**
  - Async task processing with Celery and Redis
  - Email includes post title, commenter name, and comment text
  - **Console backend for development** (emails printed to terminal)
  - **SMTP for production** (auto-configured based on DEBUG flag)

- **Architecture**
  - Django REST Framework with class-based views
  - Custom User model with email as unique identifier
  - Service-layer for business logic (users app)
  - PostgreSQL database
  - Redis for Celery message broker

## 📋 Tech Stack

- **Backend:** Django 5.2, Django REST Framework 3.14
- **Database:** PostgreSQL
- **Authentication:** SimpleJWT 5.0+
- **Task Queue:** Celery 5.2+
- **Message Broker:** Redis 4.0+
- **Python:** 3.11+

## 🛠️ Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis 4.0+
- pip or poetry

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd mini_blog
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

**Required `.env` variables:**

```env
# Database Configuration
DB_NAME=mini_blog_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Django Settings
DEBUG=True                                          # Set to False in production
SECRET_KEY=your-very-secret-key-change-this      # Use strong random string

# Email Configuration
DEFAULT_FROM_EMAIL=no-reply@mini-blog.local
BACKEND_URL=http://localhost:8000

# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

#### Email Backend Configuration

The email backend is **automatically configured** based on your `DEBUG` setting:

**Development (DEBUG=True):**
- Uses **Console Backend** — emails are printed to your terminal
- Perfect for testing without external SMTP
- No additional configuration needed ✅

**Production (DEBUG=False):**
- Uses **SMTP Backend** — emails are sent via external service
- Add these variables to `.env`:

```env
DEBUG=False
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com              # or your SMTP provider
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Use app-specific password, not actual password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
BACKEND_URL=https://yourdomain.com
```

##### Example: Gmail SMTP Configuration

1. **Enable 2-Factor Authentication** in Gmail
2. **Generate App Password:**
   - Visit [Google Account Security](https://myaccount.google.com/apppasswords)
   - Select "Mail" and "Windows Computer" (or your device)
   - Copy the 16-character password

3. **Add to `.env`:**
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your16characterapppassword
```

##### Example: SendGrid SMTP Configuration

```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.your-sendgrid-api-key
```

### 5. Set Up PostgreSQL Database

```bash
# Create database and user
createdb mini_blog_db
createuser postgres  # if not exists

# Grant privileges
psql -c "ALTER USER postgres WITH PASSWORD 'your_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE mini_blog_db TO postgres;"
```

### 6. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Start Development Server

```bash
python manage.py runserver
```

Server runs on `http://localhost:8000`

### 9. Start Celery Worker (Required for email notifications)

**In a new terminal:**

```bash
# Windows
celery -A mini_blog worker -l info -P solo

# macOS/Linux
celery -A mini_blog worker -l info
```

### 10. Start Redis (Required for Celery)

```bash
# Docker (recommended)
docker run -d -p 6379:6379 redis:latest

# Or use local Redis installation
redis-server
```

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report

# Run specific app tests
python manage.py test apps.users
python manage.py test apps.posts
python manage.py test apps.comments
```

## 📚 API Documentation

### Base URL

```
http://localhost:8000
```

### Authentication

All protected endpoints require JWT Bearer token in Authorization header:

```
Authorization: Bearer {access_token}
```

### Endpoints

#### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/signup/` | No | Create new user account |
| `GET` | `/auth/verify-email/<token>/` | No | Verify email address |
| `POST` | `/auth/login/` | No | Login and get JWT tokens |
| `GET` | `/auth/profile/` | Yes | Get authenticated user profile |

#### Posts

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/posts/` | No | List public posts (or public + own private if authenticated) |
| `POST` | `/posts/` | Yes | Create new post |
| `GET` | `/posts/<id>/` | No | Retrieve specific post (if public or owner) |
| `PATCH` | `/posts/<id>/` | Yes | Update own post |
| `DELETE` | `/posts/<id>/` | Yes | Delete own post |

#### Comments

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/posts/<id>/comments/` | Yes | Add comment to public post |
| `DELETE` | `/comments/<id>/` | Yes | Delete own comment |

---

## 🔐 Authentication Flow

### 1. Signup

**Request:**
```bash
curl -X POST http://localhost:8000/auth/signup/ \
  -H "Content-Type: application/json" \
  -d {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }
```

**Response (201):**
```json
{
  "message": "Registration successful. Please check your email to verify your account.",
  "user_id": 1
}
```

Email sent to user with verification link.

### 2. Verify Email

**Request:**
```bash
curl http://localhost:8000/auth/verify-email/{token}/
```

**Response (200):**
```json
{
  "message": "Email verified successfully."
}
```

### 3. Login

**Request:**
```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d {
    "email": "john@example.com",
    "password": "SecurePass123!"
  }
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 4. Use Access Token

**Request:**
```bash
curl http://localhost:8000/auth/profile/ \
  -H "Authorization: Bearer {access_token}"
```

**Response (200):**
```json
{
  "id": 1,
  "email": "john@example.com",
  "is_email_verified": true
}
```

---

## 📝 Usage Examples

### Create a Public Post

```bash
curl -X POST http://localhost:8000/posts/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d {
    "title": "My First Blog Post",
    "content": "This is my first blog post content.",
    "is_private": false
  }
```

### List Posts

```bash
curl http://localhost:8000/posts/
```

### Comment on a Public Post

```bash
curl -X POST http://localhost:8000/posts/1/comments/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d {
    "comment_text": "Great post! Very informative."
  }
```

Post author receives email notification with:
- Post title
- Commenter username
- Comment text

### Delete Your Comment

```bash
curl -X DELETE http://localhost:8000/comments/1/ \
  -H "Authorization: Bearer {access_token}"
```

---

## 🔧 Project Structure

```
mini_blog/
├── apps/
│   ├── users/                    # User authentication & profiles
│   │   ├── models.py            # Custom User model
│   │   ├── views.py             # Auth endpoints
│   │   ├── serializers.py       # Input validation
│   │   ├── services.py          # Business logic (signup, login, verify)
│   │   ├── utils.py             # Token generation/verification
│   │   ├── permissions.py       # Custom permissions
│   │   ├── urls.py              # Auth routes
│   │   └── tests.py             # Auth tests
│   │
│   ├── posts/                    # Blog post management
│   │   ├── models.py            # Post model
│   │   ├── views.py             # Post CRUD endpoints
│   │   ├── serializers.py       # Post serialization
│   │   ├── permissions.py       # Post ownership permissions
│   │   ├── urls.py              # Post routes
│   │   └── tests.py             # Post tests
│   │
│   └── comments/                 # Comments on posts
│       ├── models.py            # Comment model
│       ├── views.py             # Comment create/delete
│       ├── serializers.py       # Comment serialization
│       ├── tasks.py             # Celery email task
│       ├── urls.py              # Comment routes
│       └── tests.py             # Comment tests
│
├── mini_blog/                    # Django project settings
│   ├── settings/
│   │   ├── base.py             # Base settings
│   │   ├── dev.py              # Development settings
│   │   └── prod.py             # Production settings
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI application
│   ├── asgi.py                 # ASGI application
│   └── celery.py               # Celery configuration
│
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
└── README.md                    # This file
```

---

## 🚀 Production Deployment

### Environment Variables for Production

Update `.env` with production values:

```env
DEBUG=False
SECRET_KEY=generate-with-python-secrets-module
DB_HOST=production-db.example.com
DB_PASSWORD=production-secure-password
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
BACKEND_URL=https://yourdomain.com
CELERY_BROKER_URL=redis://production-redis:6379/0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Deploy with Gunicorn + Nginx

```bash
# Install Gunicorn
pip install gunicorn

# Run Gunicorn
gunicorn mini_blog.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Run Celery worker in production
celery -A mini_blog worker -l info --concurrency=4
```

### Docker Deployment

```bash
docker build -t mini-blog:latest .
docker run -d -p 8000:8000 --env-file .env mini-blog:latest
```

---

## 📊 API Response Examples

### Success Response (201 Created)

```json
{
  "id": 1,
  "author": "johndoe",
  "title": "My Post",
  "content": "Content here",
  "is_private": false,
  "created_at": "2026-06-10T12:00:00Z",
  "updated_at": "2026-06-10T12:00:00Z"
}
```

### Error Response (400 Bad Request)

```json
{
  "field_name": ["Error message describing the issue"]
}
```

### Error Response (401 Unauthorized)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Error Response (403 Forbidden)

```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## 🐛 Troubleshooting

### Email Not Sending

**Development (DEBUG=True) - Emails should print to console:**
1. Run server in terminal: `python manage.py runserver`
2. Check terminal output for email content
3. Look for lines like: `Content-Type: text/plain; charset="utf-8"`

If nothing appears:
- Verify Celery worker is running: `celery -A mini_blog worker -l info`
- Check Redis is running: `redis-cli ping` (should return `PONG`)
- Check for errors in worker logs

**Production (DEBUG=False) - SMTP configuration:**
1. **Verify SMTP credentials in `.env`:**
   ```bash
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=app-specific-password  # Not your Gmail password!
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   ```

2. **Test SMTP connection in Django shell:**
   ```bash
   python manage.py shell
   >>> from django.core.mail import send_mail
   >>> send_mail(
   ...     'Test Subject',
   ...     'Test Message',
   ...     'from@example.com',
   ...     ['to@example.com'],
   ...     fail_silently=False,
   ... )
   >>> # Should return 1 if successful
   ```

3. **Common SMTP errors:**
   - `SMTPAuthenticationError`: Wrong email/password
   - `SMTPException: SMTP AUTH extension not supported`: Check EMAIL_USE_TLS=True
   - `ConnectionRefusedError`: SMTP server unreachable (check firewall)

4. **Check Celery & Redis:**
   ```bash
   celery -A mini_blog worker -l info
   redis-cli ping
   ```

### Switching Between Email Backends

**To development (console backend):**
```env
DEBUG=True
```
Restart server - emails now print to console automatically.

**To production (SMTP backend):**
```env
DEBUG=False
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```
Restart server - emails now sent via SMTP.

### JWT Token Errors

```
"Token is invalid or expired"
```

- Access tokens expire after 180 minutes
- Use refresh token to get new access token
- See SimpleJWT documentation for refresh endpoint

### Database Connection Failed

```
psycopg2.OperationalError: could not connect to server
```

- Verify PostgreSQL is running
- Check DB credentials in `.env`
- Ensure database exists: `createdb mini_blog_db`

### Redis Connection Failed

```
ConnectionError: Error 111 connecting to localhost:6379
```

- Start Redis: `redis-server`
- Or use Docker: `docker run -d -p 6379:6379 redis:latest`

---

## 📈 Performance Tips

1. **Add Pagination:** Limit posts per page to reduce memory usage
2. **Use Indexes:** Add indexes on frequently queried fields
3. **Cache Results:** Use Redis for caching frequently accessed posts
4. **Monitor Celery:** Watch for task failures in production

---

## 🔒 Security Recommendations

1. ✅ Use HTTPS in production (set `SECURE_SSL_REDIRECT = True`)
2. ✅ Rotate `SECRET_KEY` regularly
3. ✅ Use strong database passwords
4. ✅ Enable rate limiting on auth endpoints
5. ✅ Add CORS configuration if frontend is separate
6. ✅ Validate and sanitize all user inputs
7. ✅ Use environment variables for sensitive data

---

## 📞 Support & Contribution

For issues, questions, or contributions, please open an issue on the repository.

## 📄 License

This project is licensed under the MIT License.

---

**Last Updated:** June 2026  
**Maintainer:** Ibrar Backend Dev Team
