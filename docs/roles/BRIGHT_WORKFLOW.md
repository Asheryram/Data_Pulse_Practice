# Bright Kirenga - Backend Dev 3 Workflow
## Role: Scheduling & Notifications

---

## Day 1-2: Celery Tasks Setup (Monday-Tuesday)

### Day 1: Sprint Planning & Celery Foundation (9:00 - 17:00)
- [ ] Attend sprint planning
- [ ] Commit to User Stories #7, #8 (13 story points - Stretch Goals)
- [ ] Help Yram with Celery infrastructure

**Create Celery Tasks Structure:**
```bash
cd backend/scheduling
mkdir -p management/commands
touch tasks.py
```

**Create Basic Task:**
```python
# backend/scheduling/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def test_celery():
    return "Celery is working!"

@shared_task
def send_email_task(subject, message, recipient):
    send_mail(subject, message, 'noreply@datapulse.com', [recipient])
    return f"Email sent to {recipient}"
```

**Test Celery Task:**
```python
# In Django shell
from scheduling.tasks import test_celery
result = test_celery.delay()
print(result.get())  # Should print: "Celery is working!"
```

**End of Day:**
- [ ] Celery tasks structure created
- [ ] Basic task tested
- [ ] Ready for Day 2 implementation

### Day 2: Background Task Implementation (9:00 - 17:00)

**Morning: Daily Standup**
```
Yesterday: Set up Celery task structure
Today: Implement validation and notification tasks
Blockers: None
```

**Create Validation Task:**
```python
# backend/scheduling/tasks.py
@shared_task
def run_quality_check_task(dataset_id, rule_ids):
    from checks.services.validation_engine import ValidationEngine
    from checks.services.scoring_service import calculate_quality_score
    from reports.services.report_service import generate_quality_report

    # Run validation
    engine = ValidationEngine(dataset_id)
    rules = Rule.objects.filter(id__in=rule_ids)
    results = engine.run_checks(rules)

    # Calculate score
    score = calculate_quality_score(results)

    # Generate report
    report = generate_quality_report(dataset_id, results)

    # Check for alerts
    check_and_send_alerts(dataset_id, score['score'])

    return report.id
```

**Create Notification Task:**
```python
@shared_task
def send_quality_alert_task(dataset_name, score, threshold, recipient):
    subject = f"Quality Alert: {dataset_name}"
    message = f"""
    Quality score dropped below threshold.

    Dataset: {dataset_name}
    Current Score: {score}
    Threshold: {threshold}

    Please review the dataset.
    """
    send_mail(subject, message, 'noreply@datapulse.com', [recipient])
```

**End of Day:**
- [ ] Validation task implemented
- [ ] Notification task implemented
- [ ] Tasks tested
- [ ] Update standup

---

## Day 3: Scheduling System (Wednesday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Set up Celery and notification infrastructure
Today: Implement scheduling system
Blockers: None
```

### Task #7.1: Implement Celery Beat Scheduling (9:00 - 12:00)
```bash
git checkout -b feature/celery-scheduling
cd backend/scheduling
```

**Create Schedule Model:**
```python
# backend/scheduling/models.py
from django.db import models
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

class Schedule(models.Model):
    dataset = models.ForeignKey('datasets.Dataset', on_delete=models.CASCADE)
    rules = models.ManyToManyField('rules.Rule')
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create Celery Beat periodic task
        self.create_periodic_task()

    def create_periodic_task(self):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            hour=2,
            minute=0,
        )

        PeriodicTask.objects.update_or_create(
            name=f'schedule-{self.id}',
            defaults={
                'crontab': schedule,
                'task': 'scheduling.tasks.run_quality_check_task',
                'args': json.dumps([self.dataset.id, list(self.rules.values_list('id', flat=True))]),
                'enabled': self.enabled,
            }
        )
```

**Create Periodic Task:**
```python
# backend/scheduling/tasks.py
from celery import shared_task
from celery.schedules import crontab

@shared_task
def nightly_quality_checks():
    """Run all enabled scheduled checks"""
    schedules = Schedule.objects.filter(enabled=True)

    for schedule in schedules:
        run_quality_check_task.delay(
            schedule.dataset.id,
            list(schedule.rules.values_list('id', flat=True))
        )
```

**Configure Celery Beat:**
```python
# backend/datapulse/settings/base.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'nightly-quality-checks': {
        'task': 'scheduling.tasks.nightly_quality_checks',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    },
}
```

**Commit:**
```bash
pytest tests/test_scheduling.py -v
git commit -m "feat(scheduling): implement Celery Beat scheduling"
```

### Mid-Morning: Backlog Refinement (11:00 - 12:00)
- [ ] Report progress
- [ ] Identify risks

### Afternoon: Task #7.2 & #7.3: Schedule API & Batch Processing (13:00 - 17:00)

**Task #7.2: Schedule Configuration API**
```python
# backend/scheduling/views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_schedule(request):
    # Create schedule
    # Set frequency (daily, weekly, monthly)
    # Set time
    # Link to dataset and rules
```

**Endpoints:**
```
POST   /api/schedules          - Create schedule
GET    /api/schedules          - List schedules
GET    /api/schedules/{id}     - Get schedule
PUT    /api/schedules/{id}     - Update schedule
DELETE /api/schedules/{id}     - Delete schedule
```

**Task #7.3: Batch Processing**
```python
@shared_task
def batch_process_datasets(dataset_ids: list):
    # Process multiple datasets
    # Run checks in parallel
    # Aggregate results
```

**Commit & PR:**
```bash
pytest tests/test_scheduling.py -v
git add .
git commit -m "feat(scheduling): add schedule API and batch processing"
git push origin feature/scheduling-system
gh pr create --title "feat(scheduling): implement scheduling system" --body "Closes #7.1, #7.2, #7.3"
```

**End of Day:**
- [ ] Scheduling PR submitted
- [ ] Tests passing
- [ ] Update standup

---

## Day 4: Notifications & Polish (Thursday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Completed scheduling system
Today: Implement notification system, testing
Blockers: None
```

### Task #8.1 & #8.2: Notification System (9:00 - 12:00)
```bash
git checkout -b feature/notification-system
cd backend/scheduling
```

**Implementation:**
```python
# backend/scheduling/notifications.py
from django.core.mail import send_mail

def send_quality_alert(user_email, dataset_name, score, threshold):
    subject = f"Quality Alert: {dataset_name}"
    message = f"""
    Quality score dropped below threshold.

    Dataset: {dataset_name}
    Current Score: {score}
    Threshold: {threshold}

    Please review the dataset.
    """
    send_mail(subject, message, 'noreply@datapulse.com', [user_email])
```

**Task #8.2: Alert Threshold Configuration**
```python
# backend/scheduling/models.py
class AlertConfig(models.Model):
    dataset = models.ForeignKey(Dataset)
    threshold = models.IntegerField()  # Score threshold
    notify_email = models.EmailField()
    enabled = models.BooleanField(default=True)
```

**API Endpoints:**
```
POST   /api/alerts          - Create alert config
GET    /api/alerts          - List alerts
PUT    /api/alerts/{id}     - Update alert
DELETE /api/alerts/{id}     - Delete alert
```

**Commit:**
```bash
pytest tests/test_notifications.py -v
git commit -m "feat(notifications): implement alert system"
```

### Afternoon: Task #8.3: Email Integration (13:00 - 15:00)

**Configure Email Settings:**
```python
# backend/datapulse/settings/base.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
```

**Trigger Alerts:**
```python
@shared_task
def check_and_alert(dataset_id):
    # Run quality check
    # Get score
    # Check against threshold
    # Send alert if below threshold
```

**Commit & PR:**
```bash
pytest tests/test_notifications.py -v
git add .
git commit -m "feat(notifications): add email integration"
git push origin feature/notification-system
gh pr create --title "feat(notifications): implement notification system" --body "Closes #8.1, #8.2, #8.3"
```

### Integration Testing (15:00 - 16:00)
**Work with Bernice:**
- [ ] Test scheduled execution
- [ ] Test alert triggers
- [ ] Test email sending
- [ ] Fix bugs

### Sprint Review (17:00 - 18:00)
**Demo:**
1. Create schedule for dataset
2. Show scheduled execution
3. Configure alert threshold
4. Trigger alert
5. Show email notification

### Sprint Retrospective (18:00 - 18:45)
- Reflect on sprint

---

## Implementation Examples

### Celery Configuration
```python
# backend/datapulse/celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datapulse.settings')

app = Celery('datapulse')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### Scheduled Task
```python
# backend/scheduling/tasks.py
@shared_task
def run_scheduled_check(schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    dataset = schedule.dataset
    rules = schedule.rules.all()

    # Run validation
    engine = ValidationEngine(dataset.id)
    results = engine.run_checks(rules)

    # Calculate score
    score = calculate_quality_score(results)

    # Generate report
    report = generate_quality_report(dataset.id, results)

    # Check alerts
    alerts = AlertConfig.objects.filter(dataset=dataset, enabled=True)
    for alert in alerts:
        if score['score'] < alert.threshold:
            send_quality_alert(
                alert.notify_email,
                dataset.name,
                score['score'],
                alert.threshold
            )

    return report.id
```

### Schedule Model
```python
# backend/scheduling/models.py
class Schedule(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    rules = models.ManyToManyField(Rule)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    time = models.TimeField()
    enabled = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## Success Criteria

### User Story #7: Scheduled Checks
- [x] Cron-based scheduler
- [x] Schedule configuration API
- [x] Batch processing
- [x] Tests passing

### User Story #8: Quality Alerts
- [x] Notification system
- [x] Alert threshold config
- [x] Email integration
- [x] Tests passing
