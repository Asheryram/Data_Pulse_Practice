# Diane Ishimwe - Backend Dev 2 Workflow
## Role: API & Reporting

---

## Day 1: Authentication Setup (Monday)

### Morning: Sprint Planning (9:00 - 11:00)
- [ ] Attend sprint planning
- [ ] Commit to User Stories #6, #4 (13 story points)
- [ ] Break down stories into tasks

### Afternoon: JWT Authentication (11:00 - 17:00)

**Task #6.1: Implement JWT Authentication**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/jwt-auth
cd backend/authentication
```

**Implementation:**
- Install PyJWT and passlib
- Create token generation function
- Create token verification function
- Set up password hashing

**Files to modify:**
- `backend/authentication/services.py`
- `backend/datapulse/settings/base.py`

**Commit:**
```bash
pytest tests/test_auth.py::test_jwt -v
git commit -m "feat(auth): implement JWT token system"
```

**Task #6.2: Registration Endpoint**
```python
# backend/authentication/views.py
@api_view(['POST'])
def register(request):
    # Validate input
    # Hash password
    # Create user
    # Return success
```

**Task #6.3: Login Endpoint**
```python
@api_view(['POST'])
def login(request):
    # Validate credentials
    # Generate JWT token
    # Return token + user info
```

**Commit & PR:**
```bash
pytest tests/test_auth.py -v
git add .
git commit -m "feat(auth): add registration and login endpoints"
git push origin feature/jwt-auth
gh pr create --title "feat(auth): implement JWT authentication" --body "Closes #6.1, #6.2, #6.3"
```

**End of Day:**
- [ ] Auth PR submitted
- [ ] Tests passing
- [ ] Update standup

---

## Day 2: Auth Middleware & Reports Setup (Tuesday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Implemented JWT auth, registration, login endpoints
Today: Add auth middleware, start report generation
Blockers: None
```

### Task #6.4: Authorization Middleware (9:00 - 12:00)
```bash
git checkout -b feature/auth-middleware
cd backend/authentication
```

**Implementation:**
```python
# Create middleware to protect endpoints
# Verify JWT token in request headers
# Attach user to request object
```

**Apply to endpoints:**
- `/api/datasets/*`
- `/api/rules/*`
- `/api/checks/*`
- `/api/reports/*`

**Tests:**
- Valid token access
- Invalid token rejection
- Expired token handling
- Missing token handling

**Commit & PR:**
```bash
pytest tests/test_auth.py -v
git commit -m "feat(auth): add authorization middleware"
git push origin feature/auth-middleware
gh pr create --title "feat(auth): add auth middleware" --body "Closes #6.4"
```

### Afternoon: Reports Schema & Setup (13:00 - 17:00)

**Task #4.3: Collaborate with Zainab on Reports Schema**
- Review reports table design
- Confirm fields needed
- Discuss relationships

**Start Task #4.1: Report Generation API**
```bash
git checkout -b feature/report-generation
cd backend/reports
```

**Implementation (Start):**
- Create Report model
- Create serializer
- Start report generation logic

**End of Day:**
- [ ] Auth middleware PR submitted
- [ ] Reports setup started
- [ ] Review Joseph's validation PR
- [ ] Update standup

---

## Day 3: Reporting System (Wednesday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Completed auth middleware, started report generation
Today: Complete report API, implement trend analytics
Blockers: None
```

### Task #4.1 & #4.2: Complete Report Generation (9:00 - 12:00)

**Implementation:**
```python
# backend/reports/services/report_service.py
def generate_quality_report(dataset_id: int, check_results: list) -> dict:
    # Aggregate check results
    # Generate per-rule findings
    # Calculate statistics
    # Save report to database
    # Return report data
```

**Endpoint:**
```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report(request, report_id):
    # Fetch report
    # Return detailed findings
```

**Commit:**
```bash
pytest tests/test_reports.py -v
git commit -m "feat(reports): implement quality report generation"
```

### Mid-Morning: Backlog Refinement (11:00 - 12:00)
- [ ] Report progress: 70% complete
- [ ] Identify risks

### Afternoon: Task #5.1 & #5.2: Trend Analytics (13:00 - 17:00)

**Implementation:**
```python
# backend/reports/views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trends(request):
    dataset_id = request.query_params.get('dataset_id')
    # Query historical scores
    # Aggregate by time period
    # Calculate trend direction
    # Return trend data
```

**Features:**
- Daily/weekly/monthly aggregation
- Score trend over time
- Rule-specific trends
- Improvement/decline indicators

**Commit & PR:**
```bash
pytest tests/test_reports.py -v
git add .
git commit -m "feat(reports): add trend analytics API"
git push origin feature/report-generation
gh pr create --title "feat(reports): implement reporting and trends" --body "Closes #4.1, #4.2, #5.1, #5.2"
```

**End of Day:**
- [ ] Reports PR submitted
- [ ] Integration testing scheduled
- [ ] Update standup

---

## Day 4: Integration & Polish (Thursday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Completed report generation and trend analytics
Today: Integration testing, bug fixes, documentation
Blockers: None
```

### Integration Testing (9:00 - 12:00)
**Work with Bernice:**
- [ ] Test auth flows
- [ ] Test report generation
- [ ] Test trend calculations
- [ ] Fix bugs

### Bug Fixes & Documentation (13:00 - 16:00)
- Fix any issues found
- Update API documentation
- Add usage examples
- Performance optimization

### Sprint Review (17:00 - 18:00)
**Demo:**
1. User registration
2. User login
3. Generate quality report
4. View trend analytics

### Sprint Retrospective (18:00 - 18:45)
- Reflect on sprint

---

## Implementation Examples

### JWT Authentication
```python
# backend/authentication/services.py
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)
```

### Registration Endpoint
```python
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
            password=hash_password(serializer.validated_data['password'])
        )
        return Response({'message': 'User created'}, status=201)
    return Response(serializer.errors, status=400)
```

### Report Generation
```python
def generate_quality_report(dataset_id, check_results):
    report = Report.objects.create(
        dataset_id=dataset_id,
        overall_score=calculate_score(check_results),
        total_checks=len(check_results),
        passed_checks=sum(1 for r in check_results if r['pass_rate'] == 100)
    )

    for result in check_results:
        Finding.objects.create(
            report=report,
            rule_id=result['rule_id'],
            passed=result['passed'],
            failed=result['failed'],
            pass_rate=result['pass_rate']
        )

    return report
```

---

## Success Criteria

### User Story #6: Authentication
- [x] JWT implementation
- [x] Registration endpoint
- [x] Login endpoint
- [x] Auth middleware
- [x] Tests passing

### User Story #4: Quality Reports
- [x] Report generation API
- [x] Per-rule findings
- [x] Detailed statistics
- [x] Tests passing

### User Story #5: Trends
- [x] Trend API endpoint
- [x] Historical aggregation
- [x] Time-based analysis
- [x] Tests passing
