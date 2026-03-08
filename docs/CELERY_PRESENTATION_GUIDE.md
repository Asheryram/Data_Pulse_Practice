# Celery Implementation Presentation Guide
## For Meeting with Joseph Lubandi

**Duration:** 15-20 minutes
**Goal:** Explain the problem, show the solution, get buy-in
**Your Role:** Explain and guide (not push code)

---

## Pre-Meeting Checklist

- [ ] Have VS Code open with the project
- [ ] Have `docker-compose ps` running to show services
- [ ] Have a browser tab open to `http://localhost:8000/admin`
- [ ] Have this guide open on second monitor
- [ ] Have a notepad ready for his questions

---

## PART 1: The Problem (3 minutes)

### **Opening Statement**

> "Hey Joseph, thanks for meeting! I want to talk about the CSV upload performance issue. When users upload large files, they're waiting 30-60 seconds with no feedback. I think we can fix this with Celery, and I wanted to walk you through the approach."

### **Show the Current Code**

**📁 Navigate to:** `backend/datasets/views.py`

**Find the upload function** (around line 20-40):

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_dataset(request):
    file = request.FILES.get('file')
    # ... validation ...

    dataset = Dataset.objects.create(
        name=request.data.get('name'),
        file=file,
        uploaded_by=request.user
    )

    # This is where it gets slow
    if file.name.endswith('.csv'):
        result = parse_csv(dataset.file.path)  # ← 20-30 seconds
    else:
        result = parse_json(dataset.file.path)  # ← 20-30 seconds

    dataset.row_count = result['row_count']
    dataset.save()

    return Response(DatasetSerializer(dataset).data)
```

### **Point Out the Problem**

**Say this while pointing at the code:**

> "See these lines here? When we call `parse_csv()` or `parse_json()`, the entire request is blocked. For a 50MB file, this takes 20-30 seconds. The user's browser just hangs with no feedback. That's the problem."

### **Draw the Current Flow**

**Open a whiteboard or use VS Code to draw:**

```
CURRENT FLOW (Blocking):

User clicks "Upload"
    ↓
Backend receives file
    ↓
Backend parses CSV (30 seconds) ← USER WAITS HERE
    ↓
Backend saves to database
    ↓
Backend returns response
    ↓
User sees "Upload complete" (after 30 seconds)
```

**Say:**
> "The user is stuck waiting 30 seconds. If they have a slow connection or large file, it's even worse. This is bad UX."

---

## PART 2: The Solution (5 minutes)

### **Explain Celery Concept**

**Draw the new flow:**

```
NEW FLOW (Async with Celery):

User clicks "Upload"
    ↓
Backend receives file (1 second)
    ↓
Backend saves metadata
    ↓
Backend sends task to Celery
    ↓
Backend returns response immediately ← USER GETS RESPONSE
    ↓
User sees "Processing..." (after 1 second)

Meanwhile in background:
    ↓
Celery Worker picks up task
    ↓
Celery Worker parses CSV (30 seconds)
    ↓
Celery Worker updates database
    ↓
User can poll for status
```

**Say:**
> "With Celery, we split this into two steps:
> 1. Backend receives file and returns immediately (1 second)
> 2. Celery worker processes file in background (30 seconds)
>
> User only waits 1 second instead of 30!"

### **Show the Infrastructure**

**📁 Navigate to:** `docker-compose.yml`

**Scroll to the Celery services** (around line 60-130):

```yaml
# Point to Redis
redis:
  image: redis:7-alpine
  ports: ["6379:6379"]

# Point to Celery Worker
celery:
  command: celery -A datapulse worker -l info
  environment:
    REDIS_URL: redis://redis:6379/0

# Point to Celery Beat
celery-beat:
  command: celery -A datapulse beat -l info
```

**Say:**
> "I've already set up the infrastructure. We have:
> - **Redis**: Acts as a message queue - like a mailbox for tasks
> - **Celery Worker**: Picks up tasks from Redis and executes them
> - **Celery Beat**: For scheduled tasks (we'll use this later for nightly checks)
>
> All three are running. Let me show you..."

### **Demo the Running Services**

**Open terminal and run:**

```bash
docker-compose ps
```

**Point to the output:**

```
NAME                     STATUS
datapulse-redis          Up (healthy)
datapulse-celery         Up
datapulse-celery-beat    Up
datapulse-backend        Up
```

**Say:**
> "See? All services are running and healthy. The infrastructure is ready."

---

## PART 3: The Implementation (7 minutes)

### **Step 1: Show Where Celery Config Exists**

**📁 Navigate to:** `backend/datapulse/celery.py`

**Show the file:**

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datapulse.settings.dev')

app = Celery('datapulse')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

**Say:**
> "This is the Celery configuration. It's already set up. It automatically discovers tasks from all our Django apps."

**📁 Navigate to:** `backend/datapulse/settings/base.py`

**Scroll to Celery settings** (around line 140):

```python
# --- Celery (for scheduled tasks) ---
CELERY_BROKER_URL = env("REDIS_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = env("REDIS_URL", default="redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
```

**Say:**
> "And here's the Celery configuration in settings. It's pointing to Redis. All set up."

---

### **Step 2: Explain the Task Implementation**

**📁 Navigate to:** `backend/scheduling/`

**Say:**
> "Now, here's what we need to implement. I'll walk you through the code, but I won't push it - you guys will implement it."

**Create a new file (don't save):** `backend/scheduling/tasks.py`

**Type this out while explaining:**

```python
from celery import shared_task
from datasets.models import Dataset
from datasets.services.file_parser import parse_csv, parse_json

@shared_task
def parse_uploaded_file(dataset_id):
    """
    Parse uploaded CSV/JSON file in background.
    This runs asynchronously via Celery Worker.
    """
    # Get the dataset
    dataset = Dataset.objects.get(id=dataset_id)

    # Parse based on file type
    if dataset.file.name.endswith('.csv'):
        result = parse_csv(dataset.file.path)
    else:
        result = parse_json(dataset.file.path)

    # Update dataset with results
    dataset.row_count = result['row_count']
    dataset.column_count = len(result['columns'])
    dataset.status = 'ready'  # New field we'll add
    dataset.save()

    return f"Parsed {result['row_count']} rows"
```

**Explain each part:**

1. **`@shared_task` decorator:**
   > "This decorator tells Celery this is a task it can execute. That's all you need."

2. **`dataset_id` parameter:**
   > "We pass the ID, not the object. Celery serializes to JSON, so we can't pass Django objects."

3. **The parsing logic:**
   > "This is the same logic from the view, just moved here. It runs in the background now."

4. **`status = 'ready'`:**
   > "We'll add a status field to track if parsing is done. Frontend can poll this."

---

### **Step 3: Show the Updated View**

**📁 Navigate to:** `backend/datasets/views.py`

**Say:**
> "Now, here's how the upload view changes. I'll show you the before and after."

**Show the BEFORE (current code):**

```python
@api_view(['POST'])
def upload_dataset(request):
    file = request.FILES.get('file')

    dataset = Dataset.objects.create(
        name=request.data.get('name'),
        file=file,
        uploaded_by=request.user
    )

    # BLOCKING - user waits here
    if file.name.endswith('.csv'):
        result = parse_csv(dataset.file.path)
    else:
        result = parse_json(dataset.file.path)

    dataset.row_count = result['row_count']
    dataset.save()

    return Response(DatasetSerializer(dataset).data)
```

**Now show the AFTER (type in a comment block):**

```python
# NEW VERSION WITH CELERY:

from scheduling.tasks import parse_uploaded_file

@api_view(['POST'])
def upload_dataset(request):
    file = request.FILES.get('file')

    # Save file metadata only (fast - 1 second)
    dataset = Dataset.objects.create(
        name=request.data.get('name'),
        file=file,
        uploaded_by=request.user,
        status='processing'  # New field
    )

    # Send to Celery (doesn't wait - instant)
    parse_uploaded_file.delay(dataset.id)

    # Return immediately
    return Response({
        "id": dataset.id,
        "status": "processing",
        "message": "File uploaded, parsing in background"
    })
```

**Point out the key changes:**

1. **Import the task:**
   > "We import the Celery task we created."

2. **`.delay()` method:**
   > "This is the magic. `.delay()` sends the task to Redis and returns immediately. It doesn't wait."

3. **Immediate response:**
   > "User gets a response in 1 second, not 30."

---

### **Step 4: Show the Model Change**

**📁 Navigate to:** `backend/datasets/models.py`

**Find the Dataset model** (around line 10):

**Say:**
> "We need to add a status field to track processing state."

**Show where to add:**

```python
class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10)
    row_count = models.IntegerField(default=0)
    column_count = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # ADD THIS:
    status = models.CharField(
        max_length=20,
        choices=[
            ('processing', 'Processing'),
            ('ready', 'Ready'),
            ('failed', 'Failed')
        ],
        default='processing'
    )
```

**Say:**
> "This lets us track if the file is still being parsed, ready, or failed."

---

### **Step 5: Show the Status Check Endpoint**

**📁 Stay in:** `backend/datasets/views.py`

**Say:**
> "Frontend needs a way to check if parsing is done. We add a simple status endpoint."

**Type this:**

```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_dataset_status(request, dataset_id):
    """
    Check if dataset parsing is complete.
    Frontend polls this every 2 seconds.
    """
    dataset = Dataset.objects.get(id=dataset_id)

    return Response({
        "id": dataset.id,
        "status": dataset.status,
        "row_count": dataset.row_count if dataset.status == 'ready' else None,
        "message": "Processing..." if dataset.status == 'processing' else "Ready"
    })
```

**📁 Navigate to:** `backend/datasets/urls.py`

**Show where to add the route:**

```python
urlpatterns = [
    path('upload', views.upload_dataset),
    path('<int:dataset_id>/status', views.check_dataset_status),  # ADD THIS
    # ... other routes
]
```

---

## PART 4: Live Demo (3 minutes)

### **Show It Working**

**Open terminal and run:**

```bash
# Check Celery worker is running
docker-compose logs celery --tail=20
```

**You should see:**
```
celery@... ready.
```

**Say:**
> "See? Celery worker is running and ready to accept tasks."

### **Test with curl (if you have test data)**

**Run:**

```bash
# Get auth token first
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Upload file (replace <token>)
curl -X POST http://localhost:8000/api/datasets/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@test.csv" \
  -F "name=Test Dataset"
```

**Point out:**
> "See how fast that returned? Less than 1 second. But the file is still being parsed."

**Check Celery logs:**

```bash
docker-compose logs celery --tail=10
```

**You should see:**
```
[2024-01-01 10:00:00] Received task: parse_uploaded_file[123]
[2024-01-01 10:00:05] Task parse_uploaded_file[123] succeeded
```

**Say:**
> "See? Celery picked up the task and processed it in the background."

---

## PART 5: Frontend Impact (2 minutes)

### **Explain Frontend Changes**

**Say:**
> "For the frontend, we'll need to update the upload flow. Let me show you the pseudo-code."

**Type in a new file (don't save):**

```javascript
// Frontend Upload Flow

async function uploadFile(file) {
  // 1. Upload file
  const response = await fetch('/api/datasets/upload', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });

  const { id, status } = await response.json();

  // 2. Show loading state
  showLoadingSpinner("Processing file...");

  // 3. Poll for status every 2 seconds
  const interval = setInterval(async () => {
    const statusResponse = await fetch(`/api/datasets/${id}/status`);
    const data = await statusResponse.json();

    if (data.status === 'ready') {
      clearInterval(interval);
      hideLoadingSpinner();
      showSuccess(`File processed! ${data.row_count} rows`);
    } else if (data.status === 'failed') {
      clearInterval(interval);
      hideLoadingSpinner();
      showError("File processing failed");
    }
  }, 2000);
}
```

**Say:**
> "Frontend will:
> 1. Upload file and get immediate response
> 2. Show a loading spinner
> 3. Poll the status endpoint every 2 seconds
> 4. Show success when status is 'ready'
>
> Much better UX - user knows something is happening."

---

## PART 6: Benefits & Next Steps (2 minutes)

### **Summarize the Benefits**

**Say:**
> "So to summarize, with Celery we get:
>
> ✅ **Fast response** - User waits 1 second instead of 30
> ✅ **Better UX** - User can do other things while file processes
> ✅ **Scalability** - We can add more Celery workers if needed
> ✅ **Reliability** - If worker crashes, Redis keeps the task queue
> ✅ **Future-ready** - We can use this for validation, scheduled checks, etc."

### **Address Common Questions**

**Pause and ask:**
> "What questions do you have so far?"

**Be ready for:**

**Q: "What if Celery worker crashes?"**
> "Redis keeps the task queue. When worker restarts, it picks up where it left off. We can also add retry logic to the task."

**Q: "How do we handle errors?"**
> "We wrap the task in try/except, set status to 'failed', and log the error. Frontend shows error message to user."

**Q: "Can we use this for validation too?"**
> "Absolutely! Same pattern. Validation becomes another Celery task. That's phase 2."

**Q: "Do we need to change the database?"**
> "Yes, just add the `status` field to Dataset model. One migration."

---

### **Propose Implementation Plan**

**Say:**
> "Here's what I propose:
>
> **Phase 1 (This Sprint):**
> - Add `status` field to Dataset model
> - Create `parse_uploaded_file` Celery task
> - Update upload endpoint to use Celery
> - Add status check endpoint
> - Update frontend to poll for status
>
> **Phase 2 (Next Sprint):**
> - Move validation to Celery task
> - Add scheduled checks with Celery Beat
> - Add email notifications
>
> What do you think? Should we start with Phase 1?"

---

## PART 7: Closing (1 minute)

### **Get Buy-In**

**Say:**
> "I've already set up the infrastructure - Redis, Celery Worker, and Celery Beat are all running. The hard part is done. Now it's just implementing the tasks and updating the endpoints.
>
> I can create a detailed implementation guide for you guys, or we can pair program on this if you prefer. What works better for you?"

### **Offer to Help**

**Say:**
> "I'm happy to:
> - Write the implementation guide
> - Review your PR when you implement it
> - Help debug if you run into issues
> - Pair program if you want
>
> Just let me know what you need!"

---

## Post-Meeting Actions

### **If He Says Yes:**

1. **Create implementation guide** - Detailed step-by-step for backend team
2. **Create GitHub issue** - With all the code snippets
3. **Offer to review PR** - When they implement it

### **If He Has Concerns:**

1. **Address concerns** - Listen and provide solutions
2. **Offer smaller scope** - Maybe just file parsing first
3. **Suggest pilot test** - Test with one endpoint first

### **If He Wants to Pair:**

1. **Schedule pairing session** - 1-2 hours
2. **Implement together** - You guide, he codes
3. **Test together** - Verify it works

---

## Quick Reference: Files to Show

| File | Purpose | What to Show |
|------|---------|--------------|
| `docker-compose.yml` | Infrastructure | Redis, Celery, Celery Beat services |
| `backend/datapulse/celery.py` | Celery config | Already set up |
| `backend/datapulse/settings/base.py` | Celery settings | Redis connection |
| `backend/datasets/views.py` | Current upload | The blocking code |
| `backend/datasets/models.py` | Dataset model | Where to add status field |
| `backend/scheduling/tasks.py` | New file | Where Celery task goes |

---

## Key Talking Points

✅ **Problem:** Users wait 30+ seconds for file upload
✅ **Solution:** Celery processes files in background
✅ **Benefit:** Users wait 1 second instead of 30
✅ **Infrastructure:** Already set up and running
✅ **Implementation:** Simple - just move parsing to Celery task
✅ **Frontend:** Poll for status every 2 seconds
✅ **Future:** Can use for validation, scheduled checks, notifications

---

## Confidence Boosters

**If you get nervous, remember:**

1. You've already done the hard part (infrastructure setup)
2. You understand the problem and solution
3. You're not pushing code - just explaining
4. He'll appreciate you thinking about performance
5. This is a standard pattern in Django apps

**You got this!** 🚀
