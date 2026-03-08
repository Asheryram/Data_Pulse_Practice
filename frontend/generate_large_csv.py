"""Generate a large CSV file for testing Celery performance."""

import csv
import random
from datetime import datetime, timedelta

# Configuration
OUTPUT_FILE = "large_dataset.csv"
NUM_ROWS = 1000000  # 1 million rows - will be ~100MB

print(f"Generating {NUM_ROWS:,} rows...")

# Sample data
first_names = ["John", "Jane", "Bob", "Alice", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations", "IT", "Legal", "Support", "Research"]
statuses = ["Active", "Inactive", "Pending", "Suspended"]

start_date = datetime(2020, 1, 1)

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # Header
    writer.writerow([
        "employee_id", "first_name", "last_name", "email", "age",
        "salary", "department", "city", "hire_date", "status", "performance_score"
    ])

    # Data rows
    for i in range(1, NUM_ROWS + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = f"{first.lower()}.{last.lower()}{i}@company.com"
        age = random.randint(22, 65)
        salary = random.randint(40000, 150000)
        dept = random.choice(departments)
        city = random.choice(cities)
        hire_date = (start_date + timedelta(days=random.randint(0, 1460))).strftime("%Y-%m-%d")
        status = random.choice(statuses)
        score = round(random.uniform(1.0, 5.0), 2)

        writer.writerow([i, first, last, email, age, salary, dept, city, hire_date, status, score])

        if i % 10000 == 0:
            print(f"  {i:,} rows written...")

print(f"\n✅ Done! Created {OUTPUT_FILE}")
print(f"📊 File contains {NUM_ROWS:,} rows")
print(f"📁 File size: ~{NUM_ROWS * 100 / 1024 / 1024:.1f} MB")
print(f"\n🚀 Upload this file to test Celery performance!")
