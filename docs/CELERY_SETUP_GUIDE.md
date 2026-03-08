# Quick Start Guide - DataPulse with Celery

## What Changed

### Added Services:
- ✅ **Redis** - Message broker for Celery (port 6379)
- ✅ **Celery Worker** - Runs background tasks
- ✅ **Celery Beat** - Runs scheduled tasks

### Updated Files:
- ✅ `docker-compose.yml` - Added redis, celery, celery-beat services
- ✅ `backend/requirements.txt` - Added django-celery-beat
- ✅ `backend/datapulse/celery.py` - Celery configuration (already existed)
- ✅ `backend/datapulse/__init__.py` - Imports Celery app (already existed)

---

## Setup Instructions

### 1. Update Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Add Celery Settings
Add to `backend/datapulse/settings/base.py`:
```python
# Celery Configuration
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Celery Beat
INSTALLED_APPS += ['django_celery_beat']

# Celery Beat Schedule
from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'nightly-quality-checks': {
        'task': 'scheduling.tasks.nightly_quality_checks',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    },
}
```

### 3. Run Migrations
```bash
docker-compose up -d db
docker-compose exec backend python manage.py migrate
```

### 4. Start All Services
```bash
docker-compose up --build
```

### 5. Verify Services Running
```bash
docker-compose ps
```

Should show:
- datapulse-db (PostgreSQL)
- datapulse-db-analytics (PostgreSQL Analytics)
- datapulse-redis (Redis)
- datapulse-backend (Django)
- datapulse-celery (Celery Worker)
- datapulse-celery-beat (Celery Beat)
- datapulse-etl (ETL Pipeline)
- datapulse-streamlit (Dashboard)
- datapulse-prometheus (Monitoring)
- datapulse-grafana (Visualization)

---

## Testing Celery

### Test 1: Check Celery Worker
```bash
docker-compose logs celery
```
Should see: `celery@... ready.`

### Test 2: Check Redis Connection
```bash
docker-compose exec redis redis-cli ping
```
Should return: `PONG`

### Test 3: Run a Test Task
```bash
# Enter Django shell
docker-compose exec backend python manage.py shell

# Run test task
from scheduling.tasks import test_celery
result = test_celery.delay()
print(result.get())  # Should print: "Celery is working!"
```

### Test 4: Check Celery Beat
```bash
docker-compose logs celery-beat
```
Should see scheduled tasks listed.

---

## Creating Celery Tasks

### Example Task:
```python
# backend/scheduling/tasks.py
from celery import shared_task

@shared_task
def my_background_task(param1, param2):
    # Do something that takes time
    result = param1 + param2
    return result
```

### Calling the Task:
```python
# In your view or anywhere
from scheduling.tasks import my_background_task

# Async (non-blocking)
result = my_background_task.delay(10, 20)

# Get result (blocking)
print(result.get())  # 30
```

---

## Monitoring Celery

### Option 1: Logs
```bash
# Worker logs
docker-compose logs -f celery

# Beat logs
docker-compose logs -f celery-beat
```

### Option 2: Django Admin
1. Go to http://localhost:8000/admin/
2. Navigate to "Periodic Tasks" (django-celery-beat)
3. View/manage scheduled tasks

### Option 3: Flower (Optional)
Add to docker-compose.yml:
```yaml
  flower:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: datapulse-flower
    command: celery -A datapulse flower
    ports:
      - "5555:5555"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
      - celery
    networks:
      - datapulse-network
```

Then access: http://localhost:5555

---

## Common Issues

### Issue 1: Celery worker not starting
```bash
# Check logs
docker-compose logs celery

# Restart worker
docker-compose restart celery
```

### Issue 2: Redis connection refused
```bash
# Check Redis is running
docker-compose ps redis

# Check Redis logs
docker-compose logs redis

# Restart Redis
docker-compose restart redis
```

### Issue 3: Tasks not executing
```bash
# Check worker is consuming tasks
docker-compose logs celery | grep "Received task"

# Check Redis has tasks
docker-compose exec redis redis-cli
> KEYS *
```

### Issue 4: Celery Beat not scheduling
```bash
# Check beat logs
docker-compose logs celery-beat

# Verify schedule in Django admin
# http://localhost:8000/admin/django_celery_beat/periodictask/
```

---

## Environment Variables

Add to `.env`:
```bash
# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

## Useful Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart Celery worker
docker-compose restart celery

# Restart Celery beat
docker-compose restart celery-beat

# View Celery worker logs
docker-compose logs -f celery

# View Celery beat logs
docker-compose logs -f celery-beat

# Check Redis
docker-compose exec redis redis-cli ping

# Django shell
docker-compose exec backend python manage.py shell

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

---

## Next Steps

1. ✅ Verify all services running
2. ✅ Test Celery with simple task
3. ✅ Implement file parsing task (Joseph)
4. ✅ Implement validation task (Bright)
5. ✅ Implement notification task (Bright)
6. ✅ Configure scheduled tasks (Bright)
7. ✅ Test end-to-end workflow

---

## Resources

- Celery Documentation: https://docs.celeryq.dev/
- Django Celery Beat: https://django-celery-beat.readthedocs.io/
- Redis Documentation: https://redis.io/docs/
