# Yram Asher - DevOps Engineer Workflow
## Role: Infrastructure & CI/CD

---

## Day 1: Infrastructure Setup (Monday)

### Morning: Sprint Planning (9:00 - 11:00)
- [ ] Attend sprint planning
- [ ] Understand infrastructure requirements
- [ ] Plan CI/CD pipeline
- [ ] Identify deployment needs

### Afternoon: Docker & Environment Setup (11:00 - 17:00)

**Task #1.4: Setup Celery Infrastructure**
```bash
cd devops
git checkout -b feature/celery-setup
```

**Verify docker-compose.yml has:**
- ✅ Redis service (port 6379)
- ✅ Celery worker service
- ✅ Celery beat service

**Test All Services:**
```bash
docker-compose up --build
docker-compose ps
# Should show: db, db-analytics, redis, backend, celery, celery-beat, etl, streamlit, prometheus, grafana
```

**Verify Celery Configuration:**
```bash
# Check celery.py exists
cat backend/datapulse/celery.py

# Test Celery worker
docker-compose logs celery

# Test Redis connection
docker-compose exec redis redis-cli ping
# Should return: PONG
```

**Add Celery Settings:**
```python
# backend/datapulse/settings/base.py
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Celery Beat
INSTALLED_APPS += ['django_celery_beat']
```

**Commit & PR:**
```bash
git add .
git commit -m "feat(celery): setup Celery infrastructure with Redis"
git push origin feature/celery-setup
gh pr create --title "feat(celery): add Celery and Redis" --body "Closes #1.4"
```

**Infrastructure Now Includes:**
- ✅ Redis (message broker)
- ✅ Celery worker (background tasks)
- ✅ Celery beat (scheduled tasks)
- ✅ All existing services (db, backend, etl, streamlit, prometheus, grafana)

**Setup CI/CD Pipeline:**
```bash
cd .github/workflows
# Edit ci.yml
```

**CI Pipeline (.github/workflows/ci.yml):**
```yaml
name: CI Pipeline

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: datapulse_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt

    - name: Run migrations
      run: |
        cd backend
        python manage.py migrate
      env:
        DATABASE_URL: postgresql://test:test@localhost:5432/datapulse_test

    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v --cov=. --cov-report=xml
      env:
        DATABASE_URL: postgresql://test:test@localhost:5432/datapulse_test
        REDIS_URL: redis://localhost:6379/0

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install linters
      run: |
        pip install flake8 black isort

    - name: Run flake8
      run: |
        cd backend
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

    - name: Check black formatting
      run: |
        cd backend
        black --check .

    - name: Check import sorting
      run: |
        cd backend
        isort --check-only .

  build:
    runs-on: ubuntu-latest
    needs: [test, lint]
    steps:
    - uses: actions/checkout@v3

    - name: Build Docker image
      run: |
        docker-compose build backend

    - name: Test Docker image
      run: |
        docker-compose up -d
        sleep 10
        docker-compose ps
        docker-compose down
```

**Setup Branch Protection:**
```bash
cd .github/workflows
# Create branch-protection.yml
```

**Configure GitHub Repository Settings:**
1. Go to Settings → Branches
2. Add rule for `main` branch:
   - Require PR reviews
   - Require status checks: CI Pipeline, Branch Protection
   - Require branches up to date
3. Add rule for `develop` branch:
   - Require PR reviews
   - Require status checks: CI Pipeline, Branch Protection
   - Require branches up to date

**End of Day:**
- [ ] Docker setup complete
- [ ] CI pipeline configured
- [ ] Branch protection configured
- [ ] Tests passing in CI
- [ ] Update standup

---

## Day 2: Pipeline Optimization (Tuesday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Set up Docker and CI/CD pipeline
Today: Optimize builds, configure environments, monitoring
Blockers: None
```

### Optimize Docker Build (9:00 - 11:00)

**Review Existing Dockerfile:**
Your backend/Dockerfile is already optimized:
- Uses Python 3.11-slim
- Installs only necessary dependencies
- Has entrypoint.sh for startup
- Creates uploads directory

**Verify .dockerignore exists:**
```bash
cd backend
cat .dockerignore
```

**If missing, create .dockerignore:**
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.pytest_cache/
.coverage
htmlcov/
*.log
.git
.gitignore
README.md
```

**Test Build Performance:**
```bash
time docker-compose build backend
# Measure current build time
```

**Verify All Services:**
```bash
docker-compose up -d
docker-compose ps
# Should show: db, db-analytics, backend, etl, streamlit, prometheus, grafana
```

### Environment Configuration (11:00 - 13:00)

**Create .env.example:**
```bash
# Database
DATABASE_URL=postgresql://datapulse:datapulse@db:5432/datapulse

# Redis
REDIS_URL=redis://redis:6379/0

# Django
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# File Upload
MAX_UPLOAD_SIZE=104857600  # 100MB
```

**Environment Management Script:**
```bash
#!/bin/bash
# devops/scripts/setup.sh

echo "Setting up DataPulse environment..."

# Copy env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please update with your values."
fi

# Build containers
docker-compose build

# Start services
docker-compose up -d db redis

# Wait for database
echo "Waiting for database..."
sleep 5

# Run migrations
docker-compose run --rm backend python manage.py migrate

# Create superuser
docker-compose run --rm backend python manage.py createsuperuser

# Seed data
docker-compose run --rm backend python manage.py seed_users

echo "Setup complete!"
```

### Afternoon: Monitoring Setup (13:00 - 17:00)

**Verify Existing Monitoring:**
Your docker-compose.yml already has:
- ✅ Prometheus on port 9090
- ✅ Grafana on port 3000

**Add Celery Monitoring:**
```yaml
# devops/prometheus/prometheus.yml
scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']

  - job_name: 'celery'
    static_configs:
      - targets: ['celery:5555']  # Flower monitoring
```

**Optional: Add Flower (Celery Monitoring UI):**
```yaml
# docker-compose.yml
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

**Test Monitoring:**
```bash
# Access Prometheus
curl http://localhost:9090

# Access Grafana (admin/datapulse123)
curl http://localhost:3000

# Access Flower (if added)
curl http://localhost:5555
```
```yaml
# devops/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']

  - job_name: 'postgres'
    static_configs:
      - targets: ['db:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

**End of Day:**
- [ ] Build optimization complete
- [ ] Environment management ready
- [ ] Monitoring configured
- [ ] Update standup

---

## Day 3: Deployment & Security (Wednesday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Optimized Docker builds, set up monitoring
Today: Configure staging deployment, security scanning
Blockers: None
```

### Mid-Morning: Backlog Refinement (11:00 - 12:00)
- [ ] Report infrastructure status
- [ ] Identify deployment risks

### Staging Deployment (9:00 - 13:00)

**Create Deployment Workflow:**
```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Deploy to staging
      run: |
        echo "Deploying to staging server..."
        # Add deployment commands
```

**Database Backup Script:**
```bash
#!/bin/bash
# devops/scripts/backup.sh

BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/datapulse_$TIMESTAMP.sql"

docker-compose exec -T db pg_dump -U datapulse datapulse > $BACKUP_FILE
gzip $BACKUP_FILE

echo "Backup created: $BACKUP_FILE.gz"

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
```

### Security Scanning (13:00 - 17:00)

**Add Security Checks to CI:**
```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [develop, main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Run Bandit
      run: |
        pip install bandit
        cd backend
        bandit -r . -f json -o bandit-report.json

    - name: Run Safety
      run: |
        pip install safety
        cd backend
        safety check --json

    - name: Scan Docker image
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'datapulse-backend:latest'
        format: 'sarif'
        output: 'trivy-results.sarif'
```

**End of Day:**
- [ ] Staging deployment configured
- [ ] Security scanning enabled
- [ ] Backup scripts ready
- [ ] Update standup

---

## Day 4: Production Readiness (Thursday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Configured staging and security scanning
Today: Final optimizations, documentation, monitoring
Blockers: None
```

### Performance Optimization (9:00 - 12:00)

**Database Connection Pooling:**
```python
# backend/datapulse/settings/prod.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', 5432),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

**Gunicorn Configuration:**
```python
# backend/gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50

accesslog = "-"
errorlog = "-"
loglevel = "info"
```

### Documentation (13:00 - 15:00)

**Create Deployment Guide:**
```markdown
# Deployment Guide

## Prerequisites
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

## Environment Setup
1. Clone repository
2. Copy .env.example to .env
3. Update environment variables

## Deployment Steps
1. Build containers: `docker-compose build`
2. Start services: `docker-compose up -d`
3. Run migrations: `docker-compose exec backend python manage.py migrate`
4. Create superuser: `docker-compose exec backend python manage.py createsuperuser`

## Monitoring
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Backup & Recovery
- Backup: `./devops/scripts/backup.sh`
- Restore: `./devops/scripts/restore.sh <backup-file>`
```

### Sprint Review (17:00 - 18:00)
**Demo:**
1. Show CI/CD pipeline
2. Show Docker setup
3. Show monitoring dashboards
4. Show deployment process

### Sprint Retrospective (18:00 - 18:45)
- Reflect on infrastructure work

---

## Quick Reference Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Run tests
docker-compose exec backend pytest tests/ -v

# Backup database
./devops/scripts/backup.sh

# Restart service
docker-compose restart backend

# Scale workers
docker-compose up -d --scale celery=3

# Check resource usage
docker stats
```

---

## Success Criteria

- [x] Docker infrastructure complete
- [x] CI/CD pipeline working
- [x] File storage configured
- [x] Monitoring setup
- [x] Security scanning enabled
- [x] Documentation complete
