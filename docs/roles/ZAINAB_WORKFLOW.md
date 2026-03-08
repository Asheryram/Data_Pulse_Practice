# Zainab Abdullai - Data Engineer Workflow
## Role: Schema & Data Pipeline

---

## Day 1: Database Design (Monday)

### Morning: Sprint Planning (9:00 - 11:00)
- [ ] Attend sprint planning
- [ ] Understand data requirements
- [ ] Plan database architecture
- [ ] Identify relationships

### Afternoon: Schema Design (11:00 - 17:00)

**Task #2.6: Design Rules Table Schema**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/database-schema
cd backend
```

**Create Database Schema Document:**
```markdown
# DataPulse Database Schema

## Tables Overview
1. users - User authentication
2. datasets - Uploaded files
3. rules - Validation rules
4. checks - Quality check runs
5. findings - Check results
6. reports - Quality reports
7. schedules - Scheduled checks
8. alerts - Alert configurations
```

**Users Table:**
```python
# backend/authentication/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[
        ('analyst', 'Data Analyst'),
        ('engineer', 'Data Engineer'),
        ('manager', 'Data Manager')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Datasets Table:**
```python
# backend/datasets/models.py
class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10)  # csv, json
    row_count = models.IntegerField(default=0)
    column_count = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'datasets'
        indexes = [
            models.Index(fields=['uploaded_by', '-uploaded_at']),
        ]
```

**Rules Table:**
```python
# backend/rules/models.py
class Rule(models.Model):
    RULE_TYPES = [
        ('null_check', 'Null Check'),
        ('type_check', 'Type Check'),
        ('range_check', 'Range Check'),
        ('unique_check', 'Uniqueness Check'),
    ]

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    column_name = models.CharField(max_length=255)
    parameters = models.JSONField(default=dict)  # Flexible rule config
    enabled = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rules'
        indexes = [
            models.Index(fields=['dataset', 'enabled']),
        ]
```

**Task #4.3: Design Reports Table Schema**
```python
# backend/checks/models.py
class Check(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ])
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    triggered_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'checks'
        indexes = [
            models.Index(fields=['dataset', '-started_at']),
        ]

class Finding(models.Model):
    check = models.ForeignKey(Check, on_delete=models.CASCADE, related_name='findings')
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    passed = models.IntegerField()
    failed = models.IntegerField()
    pass_rate = models.DecimalField(max_digits=5, decimal_places=2)
    failed_rows = models.JSONField(default=list)  # Store row numbers

    class Meta:
        db_table = 'findings'
        indexes = [
            models.Index(fields=['check', 'rule']),
        ]

class Report(models.Model):
    check = models.OneToOneField(Check, on_delete=models.CASCADE)
    overall_score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=1)  # A, B, C, D, F
    total_checks = models.IntegerField()
    passed_checks = models.IntegerField()
    failed_checks = models.IntegerField()
    recommendations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports'
        indexes = [
            models.Index(fields=['-created_at']),
        ]
```

**Create Migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Create ER Diagram:**
```
Users (1) ----< (M) Datasets
Datasets (1) ----< (M) Rules
Datasets (1) ----< (M) Checks
Checks (1) ----< (M) Findings
Rules (1) ----< (M) Findings
Checks (1) ---- (1) Report
```

**Commit & PR:**
```bash
git add .
git commit -m "feat(schema): design database schema for all tables"
git push origin feature/database-schema
gh pr create --title "feat(schema): implement database schema" --body "Closes #2.6, #4.3"
```

**End of Day:**
- [ ] Schema designed
- [ ] Models created
- [ ] Migrations generated
- [ ] ER diagram documented
- [ ] Update standup

---

## Day 2: Schema Implementation (Tuesday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Designed complete database schema
Today: Implement migrations, create indexes, optimize queries
Blockers: None
```

### Database Migrations (9:00 - 12:00)

**Create Initial Migration:**
```python
# backend/datasets/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='uploads/')),
                ('file_type', models.CharField(max_length=10)),
                ('row_count', models.IntegerField(default=0)),
                ('column_count', models.IntegerField(default=0)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_by', models.ForeignKey(
                    to='authentication.User',
                    on_delete=models.CASCADE
                )),
            ],
            options={
                'db_table': 'datasets',
            },
        ),
        migrations.AddIndex(
            model_name='dataset',
            index=models.Index(
                fields=['uploaded_by', '-uploaded_at'],
                name='datasets_upload_idx'
            ),
        ),
    ]
```

**Test Migrations:**
```bash
# Create test database
python manage.py migrate --database=default

# Verify tables created
python manage.py dbshell
\dt
\d datasets
```

### Performance Indexes (12:00 - 14:00)

**Add Performance Indexes:**
```python
# backend/checks/migrations/0002_add_indexes.py
class Migration(migrations.Migration):
    dependencies = [
        ('checks', '0001_initial'),
    ]

    operations = [
        # Index for finding checks by dataset and date
        migrations.AddIndex(
            model_name='check',
            index=models.Index(
                fields=['dataset', '-started_at'],
                name='checks_dataset_date_idx'
            ),
        ),
        # Index for report queries
        migrations.AddIndex(
            model_name='report',
            index=models.Index(
                fields=['-created_at', 'overall_score'],
                name='reports_date_score_idx'
            ),
        ),
        # Composite index for findings
        migrations.AddIndex(
            model_name='finding',
            index=models.Index(
                fields=['check', 'rule', 'pass_rate'],
                name='findings_composite_idx'
            ),
        ),
    ]
```

### Afternoon: Data Validation (14:00 - 17:00)

**Add Database Constraints:**
```python
# backend/datasets/migrations/0002_add_constraints.py
class Migration(migrations.Migration):
    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        # Add check constraint for row count
        migrations.AddConstraint(
            model_name='dataset',
            constraint=models.CheckConstraint(
                check=models.Q(row_count__gte=0),
                name='datasets_row_count_positive'
            ),
        ),
        # Add check constraint for column count
        migrations.AddConstraint(
            model_name='dataset',
            constraint=models.CheckConstraint(
                check=models.Q(column_count__gte=0),
                name='datasets_column_count_positive'
            ),
        ),
    ]
```

**Create Data Dictionary:**
```markdown
# Data Dictionary

## datasets
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | bigint | NO | Primary key |
| name | varchar(255) | NO | Dataset name |
| file | varchar(255) | NO | File path |
| file_type | varchar(10) | NO | csv or json |
| row_count | integer | NO | Number of rows |
| column_count | integer | NO | Number of columns |
| uploaded_by | bigint | NO | Foreign key to users |
| uploaded_at | timestamp | NO | Upload timestamp |

## rules
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | bigint | NO | Primary key |
| dataset_id | bigint | NO | Foreign key to datasets |
| rule_type | varchar(20) | NO | Type of validation |
| column_name | varchar(255) | NO | Target column |
| parameters | jsonb | NO | Rule configuration |
| enabled | boolean | NO | Active status |
| created_by | bigint | NO | Foreign key to users |
| created_at | timestamp | NO | Creation timestamp |
```

**End of Day:**
- [ ] Migrations implemented
- [ ] Indexes created
- [ ] Constraints added
- [ ] Data dictionary complete
- [ ] Update standup

---

## Day 3: Data Pipeline (Wednesday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Implemented migrations and indexes
Today: Create data pipeline for metrics and trends
Blockers: None
```

### Mid-Morning: Backlog Refinement (11:00 - 12:00)
- [ ] Report progress: 70% complete
- [ ] Identify performance bottlenecks

### Task #5.3: Create Data Pipeline (9:00 - 13:00)
```bash
git checkout -b feature/data-pipeline
cd data-engineering/pipeline
```

**ETL Pipeline:**
```python
# data-engineering/pipeline/etl_pipeline.py
import pandas as pd
from sqlalchemy import create_engine

class DataPulseETL:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)

    def extract_quality_metrics(self):
        """Extract quality metrics from database"""
        query = """
        SELECT
            d.id as dataset_id,
            d.name as dataset_name,
            c.started_at as check_date,
            r.overall_score,
            r.grade,
            r.total_checks,
            r.passed_checks,
            r.failed_checks
        FROM reports r
        JOIN checks c ON r.check_id = c.id
        JOIN datasets d ON c.dataset_id = d.id
        ORDER BY c.started_at DESC
        """
        return pd.read_sql(query, self.engine)

    def transform_for_trends(self, df):
        """Transform data for trend analysis"""
        df['check_date'] = pd.to_datetime(df['check_date'])
        df['year_month'] = df['check_date'].dt.to_period('M')

        # Calculate monthly averages
        monthly = df.groupby(['dataset_id', 'year_month']).agg({
            'overall_score': 'mean',
            'total_checks': 'sum',
            'passed_checks': 'sum',
            'failed_checks': 'sum'
        }).reset_index()

        return monthly

    def load_to_analytics(self, df):
        """Load transformed data to analytics table"""
        df.to_sql('analytics_trends', self.engine,
                  if_exists='replace', index=False)
```

**Create Analytics Schema:**
```sql
-- data-engineering/sql/analytics_schema.sql
CREATE TABLE IF NOT EXISTS analytics_trends (
    id SERIAL PRIMARY KEY,
    dataset_id BIGINT REFERENCES datasets(id),
    year_month VARCHAR(7),
    avg_score DECIMAL(5,2),
    total_checks INTEGER,
    passed_checks INTEGER,
    failed_checks INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analytics_dataset_month
ON analytics_trends(dataset_id, year_month);

-- Materialized view for dashboard
CREATE MATERIALIZED VIEW quality_dashboard AS
SELECT
    d.name as dataset_name,
    COUNT(DISTINCT c.id) as total_checks,
    AVG(r.overall_score) as avg_score,
    MAX(r.overall_score) as best_score,
    MIN(r.overall_score) as worst_score,
    MAX(c.started_at) as last_check
FROM datasets d
LEFT JOIN checks c ON d.id = c.dataset_id
LEFT JOIN reports r ON c.id = r.check_id
GROUP BY d.id, d.name;

CREATE UNIQUE INDEX idx_quality_dashboard
ON quality_dashboard(dataset_name);
```

### Afternoon: Task #5.4: Query Optimization (13:00 - 17:00)

**Optimize Trend Queries:**
```python
# backend/reports/services/report_service.py
from django.db.models import Avg, Count, Max, Min
from django.db.models.functions import TruncDate, TruncMonth

def get_quality_trends(dataset_id, period='daily'):
    """Get quality trends with optimized query"""

    if period == 'daily':
        trunc_func = TruncDate
    elif period == 'monthly':
        trunc_func = TruncMonth
    else:
        trunc_func = TruncDate

    trends = Report.objects.filter(
        check__dataset_id=dataset_id
    ).annotate(
        period=trunc_func('created_at')
    ).values('period').annotate(
        avg_score=Avg('overall_score'),
        total_checks=Count('id'),
        best_score=Max('overall_score'),
        worst_score=Min('overall_score')
    ).order_by('period')

    return list(trends)
```

**Add Database Views:**
```python
# backend/checks/migrations/0003_create_views.py
class Migration(migrations.Migration):
    dependencies = [
        ('checks', '0002_add_indexes'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE OR REPLACE VIEW dataset_summary AS
            SELECT
                d.id,
                d.name,
                COUNT(DISTINCT c.id) as total_checks,
                AVG(r.overall_score) as avg_score,
                MAX(c.started_at) as last_check
            FROM datasets d
            LEFT JOIN checks c ON d.id = c.dataset_id
            LEFT JOIN reports r ON c.id = r.check_id
            GROUP BY d.id, d.name;
            """,
            reverse_sql="DROP VIEW IF EXISTS dataset_summary;"
        ),
    ]
```

**Performance Testing:**
```python
# Test query performance
from django.test.utils import override_settings
from django.db import connection
from django.test import TestCase

class QueryPerformanceTest(TestCase):
    def test_trend_query_performance(self):
        # Create test data
        dataset = Dataset.objects.create(name='Test')

        # Measure query time
        with self.assertNumQueries(1):
            trends = get_quality_trends(dataset.id)

        # Assert query time < 100ms
        queries = connection.queries
        assert float(queries[0]['time']) < 0.1
```

**Commit & PR:**
```bash
git add .
git commit -m "feat(pipeline): create data pipeline and optimize queries"
git push origin feature/data-pipeline
gh pr create --title "feat(pipeline): implement data pipeline" --body "Closes #5.3, #5.4"
```

**End of Day:**
- [ ] Data pipeline created
- [ ] Queries optimized
- [ ] Analytics schema ready
- [ ] Update standup

---

## Day 4: Analytics & Documentation (Thursday)

### Morning: Daily Standup (7:00 - 7:15)
```
Yesterday: Created data pipeline and optimized queries
Today: Create analytics views, final optimization, documentation
Blockers: None
```

### Analytics Dashboard (9:00 - 12:00)

**Create Dashboard Queries:**
```python
# data-engineering/dashboards/quality_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

def load_data():
    engine = create_engine('postgresql://...')
    query = """
    SELECT * FROM quality_dashboard
    ORDER BY avg_score DESC
    """
    return pd.read_sql(query, engine)

def main():
    st.title('DataPulse Quality Dashboard')

    df = load_data()

    # Overall metrics
    col1, col2, col3 = st.columns(3)
    col1.metric('Total Datasets', len(df))
    col2.metric('Avg Quality Score', f"{df['avg_score'].mean():.2f}")
    col3.metric('Total Checks', df['total_checks'].sum())

    # Score distribution
    fig = px.histogram(df, x='avg_score', title='Quality Score Distribution')
    st.plotly_chart(fig)

    # Top/Bottom performers
    st.subheader('Top Performers')
    st.dataframe(df.head(10))

    st.subheader('Needs Attention')
    st.dataframe(df.tail(10))

if __name__ == '__main__':
    main()
```

### Data Archiving Strategy (12:00 - 14:00)

**Create Archiving Script:**
```python
# data-engineering/pipeline/archiving.py
from datetime import datetime, timedelta

def archive_old_data(days=90):
    """Archive data older than specified days"""
    cutoff_date = datetime.now() - timedelta(days=days)

    # Move old checks to archive table
    old_checks = Check.objects.filter(
        started_at__lt=cutoff_date
    )

    # Create archive
    for check in old_checks:
        ArchivedCheck.objects.create(
            original_id=check.id,
            dataset_id=check.dataset_id,
            data=check.to_dict(),
            archived_at=datetime.now()
        )

    # Delete from main table
    old_checks.delete()
```

### Documentation (14:00 - 16:00)

**Create Data Engineering Guide:**
```markdown
# Data Engineering Guide

## Database Schema
- See ER diagram in docs/schema.png
- See data dictionary in docs/data_dictionary.md

## ETL Pipeline
- Extract: Pull data from operational database
- Transform: Aggregate and calculate metrics
- Load: Store in analytics tables

## Query Optimization
- All queries use indexes
- Materialized views for dashboards
- Query time < 100ms for 1M rows

## Maintenance
- Run archiving monthly: `python manage.py archive_data`
- Refresh materialized views: `REFRESH MATERIALIZED VIEW quality_dashboard`
- Vacuum database weekly: `VACUUM ANALYZE`
```

### Sprint Review (17:00 - 18:00)
**Demo:**
1. Show database schema
2. Show data pipeline
3. Show analytics dashboard
4. Show query performance

### Sprint Retrospective (18:00 - 18:45)
- Reflect on data engineering work

---

## Success Criteria

- [x] Database schema designed
- [x] Migrations created
- [x] Indexes optimized
- [x] Data pipeline implemented
- [x] Analytics views created
- [x] Documentation complete
