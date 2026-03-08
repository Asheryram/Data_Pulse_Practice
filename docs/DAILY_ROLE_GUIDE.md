# DataPulse Team 9 - Daily Role Guide

## Kevin (Product Owner) - Daily Guide

### Day 1: Monday - Sprint Planning Day

**8:00 AM - Pre-Planning Prep**
- Review product backlog
- Prioritize user stories for sprint
- Prepare acceptance criteria
- Identify dependencies

**9:00 AM - Sprint Planning Meeting (2 hours)**
```
1. Present sprint goal: "Users can upload files and validate data quality"
2. Present prioritized user stories:
   - Epic #1: File Upload & Validation (Priority 1)
   - Epic #3: Authentication (Priority 2)
   - Epic #2: Reporting (Priority 3)
3. Answer team questions on requirements
4. Approve story point estimates
5. Confirm sprint commitment
```

**11:00 AM - Post-Planning**
- Create/update epics on GitHub
- Create user stories with acceptance criteria
- Label stories by priority
- Assign stories to sprint milestone

**Afternoon**
- Available for team questions
- Review and approve database schema (with Zainab)
- Clarify requirements as needed
- Update product roadmap

**End of Day Checklist:**
- [ ] Sprint backlog finalized
- [ ] All stories have clear acceptance criteria
- [ ] Team knows sprint goal
- [ ] No blocking questions

---

### Day 2: Tuesday - Development Day

**7:00 AM - Check Standup Issue**
- Read team updates
- Identify any blockers
- Note questions for follow-up

**9:00 AM - Availability Block**
- Answer requirement questions
- Review PR descriptions for business logic
- Provide feedback on UI/UX decisions

**11:00 AM - Mid-Sprint Check**
- Review GitHub project board
- Check story progress
- Identify risks to sprint goal

**2:00 PM - Stakeholder Communication**
- Update stakeholders on progress
- Gather feedback for backlog
- Prepare for next sprint

**End of Day:**
- [ ] All team questions answered
- [ ] No blockers on requirements
- [ ] Sprint on track

---

### Day 3: Wednesday - Testing Day

**7:00 AM - Check Standup Issue**

**9:00 AM - Backlog Refinement (1 hour)**
- Review next sprint stories with team
- Clarify upcoming requirements
- Adjust priorities based on progress

**11:00 AM - QA Collaboration**
- Review test results with Bernice
- Clarify expected behavior for edge cases
- Approve/reject bug severity

**Afternoon**
- Test completed features in staging
- Provide feedback on implementation
- Prepare demo scenarios

**End of Day:**
- [ ] Tested all completed stories
- [ ] Demo scenarios ready
- [ ] Next sprint stories refined

---

### Day 4: Thursday - Demo Day

**7:00 AM - Check Standup Issue**

**9:00 AM - Demo Preparation**
- Review completed stories
- Prepare demo script
- Test demo environment

**2:00 PM - Sprint Review (1 hour)**
```
1. Demo completed user stories
2. Accept/reject each story based on acceptance criteria
3. Gather feedback
4. Discuss what didn't get done
5. Update product backlog
```

**3:00 PM - Sprint Retrospective (45 min)**
```
Participate in:
- What went well
- What didn't go well
- Action items for improvement
```

**4:00 PM - Next Sprint Prep**
- Prioritize backlog for next sprint
- Create new user stories if needed
- Schedule sprint planning

**End of Day:**
- [ ] All stories accepted/rejected
- [ ] Feedback documented
- [ ] Next sprint ready

---

## Scrum Master (TBD) - Daily Guide

### Day 1: Monday - Sprint Planning Day

**8:30 AM - Pre-Planning**
- Prepare sprint planning agenda
- Review team velocity
- Check for blockers from last sprint

**9:00 AM - Facilitate Sprint Planning (2 hours)**
```
1. Review sprint goal with Kevin
2. Facilitate story estimation (Planning Poker)
3. Help team break stories into tasks
4. Ensure realistic sprint commitment
5. Assign tasks to team members
```

**11:00 AM - Setup Sprint**
- Create sprint milestone on GitHub
- Update project board
- Create shared sprint log document
- Schedule daily standups

**Afternoon**
- Check team has everything to start
- Remove any setup blockers
- Ensure CI/CD is working (with Yram)

**End of Day:**
- [ ] Sprint backlog clear
- [ ] All tasks assigned
- [ ] No blockers
- [ ] Team ready to start

---

### Day 2-3: Tuesday-Wednesday - Facilitation Days

**7:00 AM - Create Standup Issue**
```
Title: 🗣️ Standup - [Date]

Each team member post:
1. Yesterday: What I completed
2. Today: What I'm working on
3. Blockers: Any issues

@lubandi @IshimweDiane @JoeBright1619 @Kalisha1234 @Zaina-M @Asheryram
```

**8:00 AM - Review Standup Responses**
- Check all team members posted
- Identify blockers
- Note coordination needs

**9:00 AM - Remove Blockers**
- Contact team members with blockers
- Escalate to Kevin if needed
- Coordinate between team members
- Update project board

**Throughout Day**
- Monitor PR reviews (should be <4 hours)
- Check CI/CD pipeline status
- Ensure team collaboration
- Update sprint burndown

**3:00 PM - Sprint Health Check**
- Review completed vs. remaining work
- Identify risks to sprint goal
- Adjust plan if needed
- Communicate with Kevin

**End of Day:**
- [ ] All blockers addressed
- [ ] PRs being reviewed
- [ ] Sprint on track
- [ ] Team morale good

---

### Day 4: Thursday - Demo Day

**7:00 AM - Create Standup Issue**

**9:00 AM - Demo Preparation**
- Ensure demo environment ready
- Help team prepare demos
- Create demo agenda

**2:00 PM - Facilitate Sprint Review (1 hour)**
```
1. Present sprint goal and commitment
2. Facilitate demos by team
3. Capture Kevin's feedback
4. Document completed vs. planned work
5. Update velocity metrics
```

**3:00 PM - Facilitate Retrospective (45 min)**
```
1. What went well?
   - Each person shares
2. What didn't go well?
   - Each person shares
3. Action items
   - Vote on top 3
   - Assign owners
4. Close retrospective
```

**4:00 PM - Post-Sprint**
- Document retrospective actions
- Update team metrics
- Prepare for next sprint planning
- Close sprint milestone

**End of Day:**
- [ ] Retrospective complete
- [ ] Action items assigned
- [ ] Metrics updated
- [ ] Ready for next sprint

---

## Joseph Lubandi (Backend Dev 1) - Daily Guide

**Focus:** File Upload & Validation Engine

### Day 1: Monday - Planning & Setup

**9:00 AM - Sprint Planning**
- Estimate stories
- Commit to tasks:
  - Task #1.1: File upload API endpoint
  - Task #1.2: CSV parser
  - Task #1.3: JSON parser
  - Task #2.1: Validation rules CRUD
  - Task #2.2-2.5: Rule implementations
  - Task #3.1: Quality score calculator

**11:00 AM - Technical Planning**
- Review starter code
- Design file upload architecture
- Plan validation engine structure
- Coordinate with Zainab on schema

**Afternoon - Setup**
```bash
# Clone and setup
git clone <repo>
cd Data_Pulse_Practice
docker-compose up --build

# Create feature branch
git checkout -b feature/file-upload-api

# Review existing code
# - Check models
# - Check database setup
# - Review TODO comments
```

**End of Day:**
- [ ] Environment working
- [ ] Architecture planned
- [ ] First task started

---

### Day 2: Tuesday - Core Development

**7:00 AM - Post Standup**
```
Yesterday: Setup environment, planned architecture
Today: Implement file upload API and CSV parser
Blockers: None
```

**9:00 AM - File Upload API**
```python
# backend/app/api/endpoints/upload.py

@router.post("/upload")
async def upload_file(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    # Validate file type
    # Save file
    # Create database record
    # Return file info
```

**Write tests first:**
```python
# backend/tests/test_upload.py

def test_upload_csv_success():
    # Test valid CSV upload

def test_upload_invalid_format():
    # Test error handling
```

**11:00 AM - CSV Parser**
```python
# backend/app/services/parser.py

def parse_csv(file_path: str) -> pd.DataFrame:
    # Parse CSV with pandas
    # Handle errors
    # Return dataframe
```

**2:00 PM - Create PR**
```bash
git add .
git commit -m "feat(upload): add file upload API and CSV parser"
git push origin feature/file-upload-api

# Create PR
gh pr create --title "feat(upload): add file upload API" --body "Closes #1.1, #1.2"
```

**3:00 PM - Start Next Task**
```bash
git checkout develop
git pull
git checkout -b feature/json-parser
```

**End of Day:**
- [ ] File upload API complete
- [ ] CSV parser complete
- [ ] Tests passing
- [ ] PR created
- [ ] JSON parser started

---

### Day 3: Wednesday - Validation Engine

**7:00 AM - Post Standup**
```
Yesterday: Completed file upload API and CSV parser, started JSON parser
Today: Finish JSON parser, start validation rules engine
Blockers: None
```

**9:00 AM - Complete JSON Parser**
```python
def parse_json(file_path: str) -> pd.DataFrame:
    # Parse JSON
    # Convert to dataframe
    # Handle errors
```

**10:00 AM - Validation Rules CRUD**
```python
# backend/app/api/endpoints/rules.py

@router.post("/rules")
def create_rule(rule: RuleCreate, db: Session):
    # Create validation rule

@router.get("/rules/{dataset_id}")
def get_rules(dataset_id: int, db: Session):
    # Get rules for dataset
```

**1:00 PM - Implement Rule Types**
```python
# backend/app/services/validation.py

def null_check(df: pd.DataFrame, column: str) -> pd.Series:
    return df[column].notna()

def type_check(df: pd.DataFrame, column: str, expected_type: str):
    # Check data types

def range_check(df: pd.DataFrame, column: str, min_val, max_val):
    # Check value ranges

def uniqueness_check(df: pd.DataFrame, column: str):
    # Check for duplicates
```

**4:00 PM - Quality Score Calculator**
```python
def calculate_quality_score(df: pd.DataFrame, rules: List[Rule]) -> float:
    # Apply all rules
    # Count passing rows
    # Return percentage (0-100)
```

**End of Day:**
- [ ] JSON parser complete
- [ ] Validation rules CRUD complete
- [ ] All 4 rule types implemented
- [ ] Quality score calculator working
- [ ] PRs created

---

### Day 4: Thursday - Testing & Demo

**7:00 AM - Post Standup**
```
Yesterday: Completed validation engine with all rule types
Today: Final testing, bug fixes, demo prep
Blockers: None
```

**9:00 AM - Integration Testing**
```bash
# Test full flow
pytest tests/ -v --cov=app

# Fix any failing tests
# Ensure >80% coverage
```

**11:00 AM - Code Review**
- Review PRs from Diane and Bright
- Address feedback on your PRs
- Merge approved PRs

**1:00 PM - Demo Preparation**
- Prepare demo data (sample CSV)
- Test upload flow
- Test validation rules
- Test quality score

**2:00 PM - Sprint Review**
```
Demo:
1. Upload CSV file
2. Define validation rules
3. Run quality check
4. Show quality score
```

**3:00 PM - Retrospective**
- Share what went well
- Share challenges
- Suggest improvements

**End of Day:**
- [ ] All tasks complete
- [ ] Tests passing
- [ ] Demo successful
- [ ] Code merged

---

## Diane Ishimwe (Backend Dev 2) - Daily Guide

**Focus:** API & Reporting

### Day 1: Monday - Planning & Setup

**9:00 AM - Sprint Planning**
- Commit to tasks:
  - Task #6.1-6.4: Authentication system
  - Task #4.1-4.2: Quality reports
  - Task #5.1-5.2: Trend API

**Afternoon - Database Schema**
```python
# Work with Zainab on:
# - Users table
# - Reports table
# - Quality scores history table
```

**End of Day:**
- [ ] Environment setup
- [ ] Schema designed
- [ ] Auth task started

---

### Day 2: Tuesday - Authentication

**7:00 AM - Post Standup**
```
Yesterday: Setup complete, designed auth schema
Today: Implement JWT authentication
Blockers: None
```

**9:00 AM - JWT Authentication**
```python
# backend/app/core/security.py

def create_access_token(data: dict) -> str:
    # Create JWT token

def verify_token(token: str) -> dict:
    # Verify and decode token
```

**11:00 AM - Auth Endpoints**
```python
# backend/app/api/endpoints/auth.py

@router.post("/register")
def register(user: UserCreate, db: Session):
    # Hash password
    # Create user
    # Return user

@router.post("/login")
def login(credentials: OAuth2PasswordRequestForm, db: Session):
    # Verify credentials
    # Create token
    # Return token
```

**2:00 PM - Authorization Middleware**
```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify token
    # Get user from DB
    # Return user
```

**End of Day:**
- [ ] JWT auth working
- [ ] Register/login endpoints complete
- [ ] Tests passing
- [ ] PR created

---

### Day 3: Wednesday - Reporting

**7:00 AM - Post Standup**
```
Yesterday: Completed authentication system
Today: Implement quality reports and trend API
Blockers: None
```

**9:00 AM - Quality Report Generation**
```python
# backend/app/services/reports.py

def generate_quality_report(
    dataset_id: int,
    check_result_id: int,
    db: Session
) -> QualityReport:
    # Get check results
    # Generate per-rule findings
    # Calculate statistics
    # Save report
    # Return report
```

**1:00 PM - Trend API**
```python
# backend/app/api/endpoints/trends.py

@router.get("/trends/{dataset_id}")
def get_quality_trends(
    dataset_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    # Query historical scores
    # Aggregate by date
    # Return trend data
```

**End of Day:**
- [ ] Reports working
- [ ] Trends API complete
- [ ] Tests passing
- [ ] PRs created

---

### Day 4: Thursday - Polish & Demo

**7:00 AM - Post Standup**
```
Yesterday: Completed reports and trends
Today: Testing, bug fixes, demo
Blockers: None
```

**9:00 AM - Integration Testing**
- Test auth flow
- Test report generation
- Test trends API

**2:00 PM - Demo**
```
1. Register new user
2. Login and get token
3. Upload file (using Joseph's API)
4. Generate quality report
5. Show quality trends
```

**End of Day:**
- [ ] All features working
- [ ] Demo successful

---

## Bright Kirenga (Backend Dev 3) - Daily Guide

**Focus:** Scheduling & Notifications (Stretch Goals)

### Day 1-3: Support Core Features

**Tasks:**
- Help Joseph with validation engine
- Help Diane with API endpoints
- Write integration tests
- Code reviews

### Day 4: Stretch Goals (if time)

**Implement:**
- Cron-based scheduler
- Email notifications
- Batch processing

---

## Bernice Mawuena (QA Engineer) - Daily Guide

### Day 1: Monday - Test Planning

**9:00 AM - Sprint Planning**
- Understand user stories
- Note acceptance criteria

**Afternoon - Test Plan**
```markdown
# Test Plan - Sprint 1

## Test Scope
- File upload (CSV, JSON)
- Validation rules (4 types)
- Quality score calculation
- Authentication
- Reports

## Test Cases
1. File Upload
   - Valid CSV upload
   - Invalid file format
   - Large file (>10MB)
   - Empty file

2. Validation Rules
   - Null check on various columns
   - Type check (string, int, float)
   - Range check (min/max)
   - Uniqueness check

3. Quality Score
   - All rules pass (100%)
   - All rules fail (0%)
   - Mixed results (50%)
```

**End of Day:**
- [ ] Test plan complete
- [ ] Test cases documented

---

### Day 2: Tuesday - API Testing

**7:00 AM - Post Standup**
```
Yesterday: Created comprehensive test plan
Today: Write API tests for file upload
Blockers: None
```

**9:00 AM - Write API Tests**
```python
# backend/tests/test_api/test_upload.py

def test_upload_csv_success(client, test_csv_file):
    response = client.post("/upload", files={"file": test_csv_file})
    assert response.status_code == 200
    assert "file_id" in response.json()

def test_upload_invalid_format(client):
    response = client.post("/upload", files={"file": "invalid.txt"})
    assert response.status_code == 400

def test_upload_large_file(client, large_csv):
    # Test file >10MB
    pass
```

**Afternoon - Validation Tests**
```python
# backend/tests/test_validation.py

def test_null_check():
    df = pd.DataFrame({"col1": [1, None, 3]})
    result = null_check(df, "col1")
    assert result.sum() == 2  # 2 non-null values

def test_type_check():
    # Test type validation
    pass

def test_range_check():
    # Test range validation
    pass
```

**End of Day:**
- [ ] API tests written
- [ ] Validation tests written
- [ ] Tests passing

---

### Day 3: Wednesday - Integration Testing

**7:00 AM - Post Standup**
```
Yesterday: Wrote API and validation tests
Today: End-to-end integration testing
Blockers: None
```

**9:00 AM - E2E Tests**
```python
# backend/tests/test_integration/test_full_flow.py

def test_complete_validation_flow(client, db):
    # 1. Register user
    # 2. Login
    # 3. Upload file
    # 4. Create validation rules
    # 5. Run quality check
    # 6. Generate report
    # 7. Verify results
```

**Afternoon - Manual Testing**
- Test UI (if available)
- Test edge cases
- Document bugs

**Bug Report Example:**
```markdown
Title: [BUG] CSV upload fails for files with special characters

## Description
When uploading a CSV file with special characters in column names,
the parser throws an error.

## Steps to Reproduce
1. Create CSV with column name "Price ($)"
2. Upload via /upload endpoint
3. Observe error

## Expected
File should upload successfully

## Actual
500 Internal Server Error

## Severity
Medium

## Environment
- OS: Ubuntu 22.04
- Python: 3.11
- Commit: abc123
```

**End of Day:**
- [ ] E2E tests complete
- [ ] Manual testing done
- [ ] Bugs documented

---

### Day 4: Thursday - Final QA & Demo

**7:00 AM - Post Standup**
```
Yesterday: Completed integration testing, found 3 bugs
Today: Verify bug fixes, final QA, support demo
Blockers: None
```

**9:00 AM - Verify Bug Fixes**
- Retest all reported bugs
- Confirm fixes
- Close bug issues

**11:00 AM - Final QA**
- Run full test suite
- Check code coverage
- Smoke test all features

**2:00 PM - Support Demo**
- Have test data ready
- Monitor for issues
- Take notes on feedback

**3:00 PM - Retrospective**
- Share testing insights
- Suggest process improvements

**End of Day:**
- [ ] All tests passing
- [ ] Bugs verified
- [ ] Coverage >80%

---

## Yram Asher (DevOps) - Daily Guide

### Day 1: Monday - Infrastructure Setup

**9:00 AM - Sprint Planning**
- Understand infrastructure needs

**Afternoon - Docker Setup**
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: datapulse
      POSTGRES_USER: datapulse
      POSTGRES_PASSWORD: datapulse
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U datapulse"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://datapulse:datapulse@db:5432/datapulse
      SECRET_KEY: dev-secret-key
    volumes:
      - ./backend:/app
      - upload_data:/app/uploads

volumes:
  pgdata:
  upload_data:
```

**End of Day:**
- [ ] Docker setup complete
- [ ] Containers running
- [ ] Team can use docker-compose

---

### Day 2: Tuesday - CI/CD Pipeline

**7:00 AM - Post Standup**
```
Yesterday: Docker setup complete
Today: Setup CI/CD pipeline
Blockers: None
```

**9:00 AM - GitHub Actions**
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: datapulse_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -r backend/requirements.txt pytest-cov
      - name: Run tests
        run: cd backend && pytest tests/ -v --cov=app
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**End of Day:**
- [ ] CI pipeline working
- [ ] Tests run on PR
- [ ] Coverage reporting setup

---

### Day 3: Wednesday - Monitoring

**7:00 AM - Post Standup**
```
Yesterday: CI/CD pipeline complete
Today: Add monitoring, optimize Docker
Blockers: None
```

**Tasks:**
- Add health check endpoint
- Setup logging
- Optimize Docker build
- Document deployment

**End of Day:**
- [ ] Monitoring setup
- [ ] Documentation complete

---

### Day 4: Thursday - Support & Demo

**Tasks:**
- Monitor CI/CD
- Fix any pipeline issues
- Support demo
- Document lessons learned

---

## Zainab Abdullai (Data Engineer) - Daily Guide

### Day 1: Monday - Database Design

**9:00 AM - Sprint Planning**
- Understand data requirements

**Afternoon - Schema Design**
```sql
-- migrations/001_initial_schema.sql

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    row_count INTEGER,
    column_count INTEGER,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE validation_rules (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES datasets(id),
    rule_type VARCHAR(50) NOT NULL,
    column_name VARCHAR(255) NOT NULL,
    parameters JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE quality_checks (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES datasets(id),
    quality_score DECIMAL(5,2) NOT NULL,
    total_rows INTEGER NOT NULL,
    passed_rows INTEGER NOT NULL,
    failed_rows INTEGER NOT NULL,
    checked_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE quality_reports (
    id SERIAL PRIMARY KEY,
    check_id INTEGER REFERENCES quality_checks(id),
    rule_id INTEGER REFERENCES validation_rules(id),
    passed_count INTEGER NOT NULL,
    failed_count INTEGER NOT NULL,
    failure_details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_datasets_user_id ON datasets(user_id);
CREATE INDEX idx_quality_checks_dataset_id ON quality_checks(dataset_id);
CREATE INDEX idx_quality_checks_checked_at ON quality_checks(checked_at);
CREATE INDEX idx_reports_check_id ON quality_reports(check_id);
```

**End of Day:**
- [ ] Schema designed
- [ ] Migration scripts written
- [ ] Indexes planned

---

### Day 2: Tuesday - Data Pipeline

**7:00 AM - Post Standup**
```
Yesterday: Database schema complete
Today: Build data aggregation pipeline
Blockers: None
```

**9:00 AM - Aggregation Pipeline**
```python
# backend/app/services/analytics.py

def aggregate_quality_metrics(dataset_id: int, db: Session):
    """Aggregate quality metrics for dashboard"""
    query = """
    SELECT
        DATE(checked_at) as date,
        AVG(quality_score) as avg_score,
        COUNT(*) as check_count
    FROM quality_checks
    WHERE dataset_id = :dataset_id
    GROUP BY DATE(checked_at)
    ORDER BY date DESC
    LIMIT 30
    """
    return db.execute(query, {"dataset_id": dataset_id}).fetchall()
```

**End of Day:**
- [ ] Pipeline working
- [ ] Queries optimized

---

### Day 3: Wednesday - Optimization

**7:00 AM - Post Standup**
```
Yesterday: Data pipeline complete
Today: Query optimization and documentation
Blockers: None
```

**Tasks:**
- Add missing indexes
- Optimize slow queries
- Write data dictionary
- Create seed data script

**End of Day:**
- [ ] Database optimized
- [ ] Documentation complete

---

### Day 4: Thursday - Support & Demo

**Tasks:**
- Monitor database performance
- Support demo with data
- Document schema

---

**Remember:** Communication is key! Use standup issues, PR comments, and direct messages to coordinate with your team throughout the day.
