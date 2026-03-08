# How to Demonstrate Celery Workers - SLOW FILE PROCESSING

## The Problem We're Solving

**Without Celery:** User uploads 50MB CSV → waits 20-30 seconds → browser hangs → bad UX
**With Celery:** User uploads 50MB CSV → gets response in 1 second → file processes in background → good UX

---

## Setup: Open Multiple Terminal Windows

You need **3 terminal windows** side-by-side to show the full flow:

### Terminal 1: Celery Worker Logs (MOST IMPORTANT)
```bash
docker-compose logs -f celery
```

### Terminal 2: Backend Logs
```bash
docker-compose logs -f backend
```

### Terminal 3: Commands
```bash
# Keep this ready for running commands
```

---

## Demo Script for Joseph

### Step 1: Explain the Problem (30 seconds)

**Say:**
> "Joseph, imagine a user uploads a 50MB CSV file with 50,000 rows. Parsing that file takes 20-30 seconds. Without Celery, the user's browser just hangs for 30 seconds with no feedback. That's terrible UX."

**Show the code in `datasets/views.py`:**
```python
# WITHOUT CELERY (blocking):
metadata = parse_csv(file_path)  # ← User waits here for 30 seconds!
return Response(...)  # ← Response only sent after parsing
```

---

### Step 2: Show the Solution (30 seconds)

**Say:**
> "With Celery, we split this into two steps:
> 1. Backend saves the file and returns immediately (1 second)
> 2. Celery worker parses the file in the background (30 seconds)
>
> The user only waits 1 second!"

**Show the code:**
```python
# WITH CELERY (non-blocking):
demo_parse_file.delay(dataset.id, filename)  # ← Sends to Celery, doesn't wait
return Response(...)  # ← Returns immediately!
```

---

### Step 3: Live Demo (2 minutes)

#### 3a. Show Services Running
In Terminal 3:
```bash
docker-compose ps
```

**Point out:**
- ✅ `datapulse-celery` - The worker that will process files
- ✅ `datapulse-redis` - The message queue
- ✅ `datapulse-backend` - The API server

#### 3b. Show Celery Worker is Ready
In Terminal 1 (Celery logs), you should see:
```
celery@xxx ready.
```

**Say:**
> "The Celery worker is idle, waiting for tasks."

#### 3c. Upload a File

**Option A: Using Frontend (Recommended)**
1. Open `frontend/index.html` in browser
2. Login with your credentials
3. Upload `sample.csv`
4. **IMMEDIATELY point to Terminal 2**

**Option B: Using curl**
```bash
curl -X POST http://localhost:8000/api/datasets/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@frontend/sample.csv"
```

#### 3d. Watch the Magic! 🎩✨

**In Terminal 2 (Backend) - IMMEDIATE:**
```
POST /api/datasets/upload 201 Created (0.5s)
```

**Say:**
> "See? The backend returned 201 Created in half a second! The user got their response immediately."

**In Terminal 1 (Celery Worker) - BACKGROUND:**
```
============================================================
[CELERY WORKER] 🚀 Starting to parse dataset 1: sample.csv
[CELERY WORKER] ⏳ This will take 20-30 seconds...
============================================================

[CELERY WORKER] 📊 Processing... 0/25 seconds elapsed
[CELERY WORKER] 📊 Processing... 5/25 seconds elapsed
[CELERY WORKER] 📊 Processing... 10/25 seconds elapsed
[CELERY WORKER] 📊 Processing... 15/25 seconds elapsed
[CELERY WORKER] 📊 Processing... 20/25 seconds elapsed

============================================================
[CELERY WORKER] ✅ Finished parsing dataset 1
[CELERY WORKER] 📈 Parsed 50,000 rows in 25 seconds
============================================================

Task demo_parse_file[xxx] succeeded in 25.123s
```

**Say:**
> "Meanwhile, the Celery worker is processing the file in the background. It takes 20-30 seconds, but the user doesn't wait for it. They can continue using the app!"

---

## Key Points to Emphasize

### 1. **User Experience**
- ❌ Without Celery: User waits 30 seconds, browser hangs
- ✅ With Celery: User waits 1 second, gets immediate feedback

### 2. **Separation of Concerns**
- **Backend (Django):** Handles HTTP requests, returns fast
- **Worker (Celery):** Handles heavy processing, runs in background
- **Queue (Redis):** Connects them, stores pending tasks

### 3. **Scalability**
- Can run multiple Celery workers
- 10 uploads = distributed across workers
- Backend never gets blocked

### 4. **Real-World Use Cases**
- Large CSV parsing (our case)
- Sending bulk emails
- Generating reports
- Image processing
- Data exports

---

## Comparison Table

| Metric | Without Celery | With Celery |
|--------|----------------|-------------|
| User wait time | 30 seconds | 1 second |
| Backend blocked? | Yes | No |
| Can handle concurrent uploads? | No (blocks) | Yes (queues) |
| User feedback | None (hangs) | Immediate |
| Scalable? | No | Yes |

---

## Questions Joseph Might Ask

### Q: "What if the Celery worker crashes?"
**A:** Redis persists the task queue. When the worker restarts, it picks up where it left off.

### Q: "How do we notify the user when processing is done?"
**A:** Three options:
1. Frontend polls the API every few seconds
2. WebSockets for real-time updates
3. Email notification when done

### Q: "Can we see the task status?"
**A:** Yes! We can query Celery's result backend or add a `status` field to the Dataset model.

### Q: "What if we need to process 100 files at once?"
**A:** Scale horizontally - run 5-10 Celery workers. Redis distributes tasks automatically.

---

## After the Demo

**Say:**
> "So that's Celery! The infrastructure is already set up. Now we just need to:
> 1. Move the parsing logic from the view to a Celery task
> 2. Add a status field to track processing state
> 3. Update the frontend to poll for completion
>
> I can help you implement this, or you can take it from here. What do you think?"

---

## Quick Reference Commands

```bash
# Restart services after code changes
docker-compose restart backend celery

# View Celery logs
docker-compose logs -f celery

# Check Redis connection
docker exec -it datapulse-redis redis-cli ping

# See all running services
docker-compose ps

# Stop everything
docker-compose down
```
