# Bernice Mawuena - QA Engineer Workflow
## Role: Testing & Quality Assurance

---

## Day 1: Test Setup (Monday)

### Morning: Sprint Planning (9:00 - 11:00)
- [ ] Attend sprint planning
- [ ] Understand all user stories
- [ ] Identify testing requirements
- [ ] Plan test strategy

### Afternoon: Test Environment Setup (11:00 - 17:00)

**Setup Testing Framework:**
```bash
cd backend
# Install testing dependencies
pip install pytest pytest-cov pytest-django requests

# Verify test setup
pytest --version
```

**Create Test Data Files:**
```bash
cd qa/test-data
```

**valid_test.csv:**
```csv
id,name,age,email,salary
1,John Doe,30,john@example.com,50000
2,Jane Smith,25,jane@example.com,60000
3,Bob Johnson,35,bob@example.com,55000
```

**invalid_test.csv:**
```csv
id,name,age,email,salary
1,John Doe,30,john@example.com,50000
2,Jane Smith,invalid,jane@example.com,60000
3,Bob Johnson,35,invalid-email,55000
4,,,missing@example.com,
```

**valid_test.json:**
```json
[
  {"id": 1, "name": "John", "age": 30, "email": "john@example.com"},
  {"id": 2, "name": "Jane", "age": 25, "email": "jane@example.com"}
]
```

**invalid_test.json:**
```json
[
  {"id": 1, "name": "John", "age": "invalid"},
  {"id": 2, "email": "missing-name"}
]
```

**Create Test Plan:**
```bash
cd qa/test-plan
# Create test_plan.md
```

**Test Plan Structure:**
- Feature: File Upload
- Feature: Validation Rules
- Feature: Quality Scoring
- Feature: Authentication
- Feature: Reporting
- Feature: Scheduling (Stretch)

**End of Day:**
- [ ] Test environment ready
- [ ] Test data created
- [ ] Test plan documented
- [ ] Update standup

---

## Day 2: Core Feature Testing (Tuesday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Set up test environment and created test data
Today: Test file upload, authentication, validation rules
Blockers: None
```

### Task #1.5: Test File Upload (9:00 - 11:00)

**Test Cases:**
```python
# backend/tests/test_upload.py
import pytest
from rest_framework.test import APIClient

class TestFileUpload:
    def setup_method(self):
        self.client = APIClient()
        self.user = create_test_user()
        self.client.force_authenticate(user=self.user)

    def test_upload_valid_csv(self):
        # Test uploading valid CSV file
        with open('qa/test-data/valid_test.csv', 'rb') as f:
            response = self.client.post('/api/datasets/upload', {
                'name': 'Test Dataset',
                'file': f
            })
        assert response.status_code == 201
        assert 'id' in response.data

    def test_upload_invalid_format(self):
        # Test uploading invalid file format
        with open('test.txt', 'rb') as f:
            response = self.client.post('/api/datasets/upload', {
                'name': 'Test',
                'file': f
            })
        assert response.status_code == 400

    def test_upload_without_auth(self):
        # Test upload without authentication
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/datasets/upload', {})
        assert response.status_code == 401

    def test_upload_large_file(self):
        # Test uploading file >10MB
        pass

    def test_upload_empty_file(self):
        # Test uploading empty file
        pass
```

**Run Tests:**
```bash
pytest tests/test_upload.py -v --cov=datasets
```

**Document Results:**
- Create bug reports for failures
- Update test plan with results

### Afternoon: Task #6.5: Test Authentication (13:00 - 15:00)

**Test Cases:**
```python
# backend/tests/test_auth.py
class TestAuthentication:
    def test_user_registration(self):
        # Test successful registration
        response = self.client.post('/api/auth/register', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!'
        })
        assert response.status_code == 201

    def test_duplicate_registration(self):
        # Test registering with existing email
        pass

    def test_weak_password(self):
        # Test registration with weak password
        pass

    def test_user_login(self):
        # Test successful login
        response = self.client.post('/api/auth/login', {
            'email': 'test@example.com',
            'password': 'SecurePass123!'
        })
        assert response.status_code == 200
        assert 'token' in response.data

    def test_invalid_credentials(self):
        # Test login with wrong password
        pass

    def test_token_expiration(self):
        # Test expired token handling
        pass
```

**Run Tests:**
```bash
pytest tests/test_auth.py -v --cov=authentication
```

### Evening: Task #2.7: Test Validation Rules (15:00 - 17:00)

**Test Cases:**
```python
# backend/tests/test_validation_engine.py
class TestValidationEngine:
    def test_null_check_pass(self):
        # Test null check with no nulls
        pass

    def test_null_check_fail(self):
        # Test null check with nulls present
        pass

    def test_type_check_integer(self):
        # Test type check for integer column
        pass

    def test_type_check_fail(self):
        # Test type check with invalid types
        pass

    def test_range_check_pass(self):
        # Test range check within bounds
        pass

    def test_range_check_fail(self):
        # Test range check outside bounds
        pass

    def test_unique_check_pass(self):
        # Test uniqueness with no duplicates
        pass

    def test_unique_check_fail(self):
        # Test uniqueness with duplicates
        pass
```

**Edge Cases to Test:**
- Empty dataset
- Single row dataset
- All null values
- Mixed data types
- Boundary values (min/max)
- Special characters
- Unicode characters

**End of Day:**
- [ ] All core feature tests written
- [ ] Test results documented
- [ ] Bugs reported
- [ ] Update standup

---

## Day 3: Integration Testing (Wednesday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Tested upload, auth, validation rules - found 3 bugs
Today: Integration testing, test scoring and reports
Blockers: Bug #X blocking upload test
```

### Mid-Morning: Backlog Refinement (11:00 - 12:00)
- [ ] Report testing progress
- [ ] Identify critical bugs
- [ ] Prioritize bug fixes

### Task #3.3: Test Quality Score Calculation (9:00 - 11:00)

**Test Cases:**
```python
# backend/tests/test_scoring.py
class TestQualityScore:
    def test_perfect_score(self):
        # All checks pass = 100 score
        results = [
            {'passed': 100, 'failed': 0, 'pass_rate': 100},
            {'passed': 100, 'failed': 0, 'pass_rate': 100}
        ]
        score = calculate_quality_score(results)
        assert score['score'] == 100
        assert score['grade'] == 'A'

    def test_zero_score(self):
        # All checks fail = 0 score
        pass

    def test_mixed_score(self):
        # Mixed results = weighted score
        pass

    def test_empty_results(self):
        # No checks = 0 score
        pass
```

### Afternoon: Task #4.4 & #5.5: Test Reports & Trends (13:00 - 17:00)

**Test Cases:**
```python
# backend/tests/test_reports.py
class TestReports:
    def test_generate_report(self):
        # Test report generation
        pass

    def test_report_details(self):
        # Test report contains all findings
        pass

    def test_trend_calculation(self):
        # Test trend over time
        pass

    def test_trend_aggregation(self):
        # Test daily/weekly/monthly aggregation
        pass
```

**End-to-End Integration Tests:**
```python
# backend/tests/test_integration.py
class TestEndToEnd:
    def test_complete_workflow(self):
        # 1. Register user
        # 2. Login
        # 3. Upload dataset
        # 4. Create validation rules
        # 5. Run quality check
        # 6. Generate report
        # 7. View trends
        pass
```

**Run Full Test Suite:**
```bash
pytest tests/ -v --cov=. --cov-report=html
```

**End of Day:**
- [ ] Integration tests complete
- [ ] Coverage report generated
- [ ] Critical bugs identified
- [ ] Update standup

---

## Day 4: Final QA & Bug Verification (Thursday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Completed integration testing, 85% coverage
Today: Bug verification, regression testing, stretch goal testing
Blockers: None
```

### Bug Verification (9:00 - 12:00)

**Bug Verification Checklist:**
- [ ] Bug #1: File upload encoding issue - FIXED
- [ ] Bug #2: Null check false positive - FIXED
- [ ] Bug #3: Token expiration not handled - FIXED

**Regression Testing:**
```bash
# Re-run all tests to ensure fixes didn't break anything
pytest tests/ -v
```

### Stretch Goals Testing (13:00 - 15:00)

**Task #7.4: Test Scheduled Execution**
```python
# backend/tests/test_scheduling.py
class TestScheduling:
    def test_create_schedule(self):
        # Test creating schedule
        pass

    def test_schedule_execution(self):
        # Test scheduled task runs
        pass

    def test_batch_processing(self):
        # Test multiple datasets
        pass
```

**Task #8.4: Test Alert Triggers**
```python
# backend/tests/test_notifications.py
class TestNotifications:
    def test_alert_creation(self):
        # Test creating alert config
        pass

    def test_alert_trigger(self):
        # Test alert fires when threshold crossed
        pass

    def test_email_sending(self):
        # Test email is sent
        pass
```

### Performance Testing (15:00 - 16:00)

**Performance Test Cases:**
```python
def test_large_dataset_upload():
    # Upload 100MB file
    # Measure time
    # Assert < 30 seconds
    pass

def test_concurrent_uploads():
    # 10 simultaneous uploads
    # Measure throughput
    pass

def test_validation_performance():
    # Validate 1M rows
    # Assert < 60 seconds
    pass
```

### Final Test Report (16:00 - 17:00)

**Create Test Summary:**
```markdown
# Test Summary Report

## Test Coverage
- Total Tests: 87
- Passed: 85
- Failed: 2
- Coverage: 85%

## Features Tested
- [x] File Upload (12 tests)
- [x] Authentication (15 tests)
- [x] Validation Rules (20 tests)
- [x] Quality Scoring (10 tests)
- [x] Reporting (15 tests)
- [x] Trends (10 tests)
- [x] Scheduling (3 tests)
- [x] Notifications (2 tests)

## Bugs Found
- Total: 8
- Critical: 1 (FIXED)
- High: 2 (FIXED)
- Medium: 3 (FIXED)
- Low: 2 (OPEN)

## Performance Results
- Upload 10MB file: 5s
- Validate 100K rows: 12s
- Generate report: 2s

## Recommendations
- Optimize validation for large datasets
- Add caching for trend queries
- Implement rate limiting
```

### Sprint Review (17:00 - 18:00)
- Present test results
- Demo test coverage
- Show bug tracking

### Sprint Retrospective (18:00 - 18:45)
- Reflect on testing process

---

## Testing Tools & Commands

### Run Specific Tests
```bash
# Run single test file
pytest tests/test_upload.py -v

# Run specific test
pytest tests/test_upload.py::TestFileUpload::test_upload_valid_csv -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run only failed tests
pytest --lf

# Run in parallel
pytest -n 4
```

### API Testing with Postman/curl
```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'

# Upload file
curl -X POST http://localhost:8000/api/datasets/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@test.csv" \
  -F "name=Test Dataset"
```

---

## Bug Report Template

```markdown
## Bug #X: [Title]

**Severity:** Critical/High/Medium/Low
**Priority:** P0/P1/P2/P3
**Status:** Open/In Progress/Fixed/Closed

**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Result:**
What should happen

**Actual Result:**
What actually happens

**Environment:**
- OS: Windows/Linux/Mac
- Browser: Chrome/Firefox
- API Version: v1

**Screenshots/Logs:**
Attach relevant files

**Assigned To:** Developer name
```

---

## Success Criteria

- [x] All core features tested
- [x] 80%+ code coverage
- [x] All critical bugs fixed
- [x] Integration tests passing
- [x] Performance benchmarks met
- [x] Test documentation complete
