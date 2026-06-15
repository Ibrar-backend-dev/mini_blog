# Mini Blog Backend API

## Dependencies

- Python 3.11.9
- Django 5.2
- djangorestframework 3.14
- django-filter
- psycopg2-binary
- celery
- redis

## Project setup

1. Clone repository:

   ```bash
   git clone https://github.com/Ibrar-backend-dev/mini_blog.git
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
# Only required if you run Celery in normal async mode
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
```

> Note: For local development, this project currently uses Celery eager mode in `mini_blog/settings/dev.py`.
> This means tasks are executed immediately in the same Django process and you can use `python manage.py runserver` without starting a separate Celery worker.

## Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run Django server in development

```bash
python manage.py runserver
```

### Development mode behavior

In development, `CELERY_TASK_ALWAYS_EAGER = True` and `CELERY_TASK_EAGER_PROPAGATES = True` are set in `mini_blog/settings/dev.py`.

That means:

- `task.delay(...)` still triggers the task
- the task runs immediately and synchronously inside Django
- no separate Celery worker is required for local testing
- no Redis broker is needed for that eager-mode flow

### Important production warning

Eager mode is only for development and testing.

Do not use eager mode in production because:

- tasks are not processed in the background
- requests wait until the task completes
- failed tasks do not behave like real async retries
- there is no persistence or broker-managed delivery

## Normal async Celery setup (production)

If you want real background task execution, use a broker and worker instead of eager mode.

> In production, remove eager mode from your production settings and run a broker plus worker.

### Redis / Memurai broker setup

Celery requires a broker before it can run tasks.

### Option 1: Use local Redis (recommended)

If Redis is installed locally:

```bash
redis-server
```

Then run the Celery worker:

```bash
celery -A mini_blog worker -l info -P solo
```

### Option 2: Use local Memurai on Windows

If you are on Windows and do not have Redis, install Memurai and start it.

- Install Memurai from [https://www.memurai.com/](https://www.memurai.com/)
- Start the Memurai service or run Memurai so it listens on `127.0.0.1:6379`

Then use the same Celery environment values as Redis:

```bash
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
```

Start the worker:

```bash
celery -A mini_blog worker -l info -P solo
```

### Option 3: Use Docker

If Docker is available, you can run Redis in a container:

```bash
docker run -d --name mini_blog_redis -p 6379:6379 redis:latest
```

Then set the same broker values and start Celery:

```bash
celery -A mini_blog worker -l info -P solo
```

### Running the broker and worker together

For normal Celery usage, the order is:

```bash
# start broker first
redis-server
# or start Memurai if using Memurai instead of Redis

# then run Celery worker
celery -A mini_blog worker -l info -P solo
```

### Recommended terminal setup for real async Celery

When you run the app locally without Docker, you typically use three terminals:

1. Broker terminal
   - `redis-server` or the Memurai service
2. Celery worker terminal
   - `celery -A mini_blog worker -l info -P solo`
3. Django server terminal
   - `python manage.py runserver`

If your broker runs as a background service, you can reduce this to two terminals.

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

## Project folder structure

```text
mini_blog/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── manage.py
├── requirements.txt
├── apps/
│   ├── comments/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── migrations/
│   │       ├── __init__.py
│   │       └── 0001_initial.py
│   ├── posts/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── migrations/
│   │       ├── __init__.py
│   │       ├── 0001_initial.py
│   │       └── 0002_alter_post_options.py
│   └── users/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── services.py
│       ├── urls.py
│       ├── utils.py
│       ├── views.py
│       └── migrations/
│           ├── __init__.py
│           └── 0001_initial.py
├── mini_blog/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
└── venv/
```
