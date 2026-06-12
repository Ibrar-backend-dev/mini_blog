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
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
```

> Note: This project expects a Redis-compatible broker. You can use Redis directly or Memurai on Windows, because Memurai speaks the same Redis protocol.

## Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run Django server

```bash
python manage.py runserver
```

## Redis / Memurai broker setup

Celery requires a broker before it can run tasks. If Redis is not available, Memurai is the recommended Windows-compatible alternative.

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

### If you do not have Docker

If Docker is not installed, use either local Redis or local Memurai.

- On Linux/macOS: install Redis directly (`redis-server`)
- On Windows: install Memurai and configure it to bind to `127.0.0.1:6379`

## Run Celery with tasks

Always start the broker before starting the worker.

```bash
# start broker first
redis-server
# or start Memurai if using Memurai instead of Redis

# then run Celery worker
celery -A mini_blog worker -l info -P solo
```

### Recommended terminal setup (no Docker)

When you are running the app locally without Docker, you typically need three terminal sessions at once:

1. Broker terminal
   - `redis-server` or the Memurai service
2. Celery worker terminal
   - `celery -A mini_blog worker -l info -P solo`
3. Django server terminal
   - `python manage.py runserver`

This is the simplest setup because each process stays running and logs separately.

### Ways to optimize terminal usage

- Use separate terminal tabs or panes in Windows Terminal, PowerShell, or any terminal emulator.
- On Linux/macOS, you can also use a multiplexer such as `tmux` or `screen`.
- On Windows, start Redis/Memurai as a background service if available, then only keep two terminals open:
  - one for the Celery worker
  - one for `runserver`
- If you use Docker, the broker can run inside a container, so you still need two terminals:
  - one for the Celery worker
  - one for `runserver`

### Example optimized flow without Docker

1. Open terminal A, start Redis/Memurai:

   ```bash
   redis-server
   ```

2. Open terminal B, start Celery:

   ```bash
   celery -A mini_blog worker -l info -P solo
   ```

3. Open terminal C, start Django:

   ```bash
   python manage.py runserver
   ```

### Don't forget to activate venv in each terminal if not already done

- terminal B: `python manage.py runserver`

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
