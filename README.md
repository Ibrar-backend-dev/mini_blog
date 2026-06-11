# Mini Blog Backend API

## Dependencies

- Python 3.11+
- Django 5.2
- djangorestframework 3.14
- django-filter
- psycopg2-binary
- celery
- redis

## Project setup

1. Clone repository:
   ```bash
   git clone https://github.com/Ibrar-backend-dev/miniBlog.git
   cd mini_blog
   ```
2. Create virtual environment and activate:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## .env setup

Copy `.env.example` to `.env` and update the required values:

```bash
copy .env.example .env
```

Required `.env` values:

```env
DB_NAME=mini_blog_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
SECRET_KEY=your-secret-key
DEFAULT_FROM_EMAIL=no-reply@mini-blog.local
BACKEND_URL=http://localhost:8000
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

## Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run Django server

```bash
python manage.py runserver
```

## Run Celery

Start Redis first and then run the Celery worker:

```bash
redis-server
celery -A mini_blog worker -l info -P solo
```

## API usage

### Authentication

- `POST /auth/signup/`
- `GET /auth/verify-email/<token>/`
- `POST /auth/login/`
- `GET /auth/profile/`

### Posts

- `GET /posts/`
- `POST /posts/`
- `GET /posts/<id>/`
- `PATCH /posts/<id>/`
- `DELETE /posts/<id>/`

### Comments

- `POST /posts/<id>/comments/`
- `DELETE /comments/<id>/`
