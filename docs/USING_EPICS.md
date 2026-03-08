# Using Epics in DataPulse

## What is an Epic?

An **Epic** is a large body of work that can be broken down into multiple **User Stories**. It represents a major feature or initiative that typically spans multiple sprints.

## Hierarchy

```
Epic (Parent)
├── User Story 1 (Child)
│   ├── Task 1.1
│   ├── Task 1.2
│   └── Task 1.3
├── User Story 2 (Child)
│   ├── Task 2.1
│   └── Task 2.2
└── User Story 3 (Child)
    ├── Task 3.1
    └── Task 3.2
```

## When to Create an Epic

Create an Epic when:
- Feature is too large for one sprint (>21 story points)
- Multiple related user stories share a common goal
- Feature requires coordination across multiple team members
- Work spans 2+ sprints

## DataPulse Epics

### Epic #1: File Upload & Validation System
**Total: 26 story points | Sprints: 1-2**

```
Epic #1: File Upload & Validation System
├── Story #11: CSV File Upload (8 pts)
├── Story #12: JSON File Upload (5 pts)
├── Story #13: Validation Rules Engine (13 pts)
└── Story #14: Quality Score Calculation (5 pts)
```

### Epic #2: Reporting & Analytics
**Total: 16 story points | Sprint: 2**

```
Epic #2: Reporting & Analytics
├── Story #21: Quality Reports (8 pts)
└── Story #22: Trend Dashboard (8 pts)
```

### Epic #3: Authentication & Security
**Total: 5 story points | Sprint: 1**

```
Epic #3: Authentication & Security
└── Story #31: User Authentication (5 pts)
```

### Epic #4: Scheduling & Notifications (Stretch)
**Total: 13 story points | Sprint: 3**

```
Epic #4: Scheduling & Notifications
├── Story #41: Scheduled Checks (8 pts)
└── Story #42: Quality Alerts (5 pts)
```

## How to Create an Epic

### Step 1: Product Owner Creates Epic Issue

```markdown
Title: [EPIC] File Upload & Validation System

## Epic Overview
Build a complete system for uploading data files and validating them
against user-defined rules with quality scoring.

## Business Value
Enables users to assess data quality automatically, saving hours of
manual validation work.

## User Stories
- [ ] #11 - CSV File Upload
- [ ] #12 - JSON File Upload
- [ ] #13 - Validation Rules Engine
- [ ] #14 - Quality Score Calculation

## Acceptance Criteria
- Users can upload CSV and JSON files
- Users can define 4 types of validation rules
- System calculates quality score (0-100)
- All files stored securely

## Story Points Total
26 points

## Target Sprint
Sprint 1-2

## Dependencies
None

## Notes
Priority 1 for MVP. Must be complete before reporting features.
```

### Step 2: Create User Stories Under Epic

Each user story references the epic:

```markdown
Title: As a Data Analyst, I want to upload CSV files

## User Story
As a Data Analyst,
I want to upload CSV files through the web interface,
So that I can validate my data quality.

## Part of Epic
#1 - File Upload & Validation System

## Acceptance Criteria
- [ ] Given a valid CSV file, when I upload it, then it's stored successfully
- [ ] Given an invalid CSV, when I upload it, then I see a clear error message
- [ ] Given a large file (>10MB), when I upload it, then it processes without timeout

## Story Points
8

## Sprint
Sprint 1
```

### Step 3: Link Stories to Epic

In each user story, add:
```
Part of #1
```

Or in the Epic, check off stories as they're completed:
```
- [x] #11 - CSV File Upload (Done)
- [ ] #12 - JSON File Upload (In Progress)
- [ ] #13 - Validation Rules Engine (To Do)
```

## Tracking Epic Progress

### On GitHub Project Board

**Option 1: Use Milestones**
1. Create milestone: "Epic 1: File Upload & Validation"
2. Assign all related user stories to this milestone
3. GitHub shows progress: "3/4 issues closed"

**Option 2: Use Labels**
1. Create label: `epic: file-upload`
2. Tag all related stories with this label
3. Filter board by label to see epic progress

**Option 3: Manual Tracking**
Update epic issue description with checkboxes:
```
## Progress
- [x] Story #11 - CSV Upload (Done)
- [x] Story #12 - JSON Upload (Done)
- [ ] Story #13 - Validation Rules (In Progress)
- [ ] Story #14 - Quality Score (To Do)

Progress: 50% (2/4 stories complete)
```

## Epic Workflow

### Sprint Planning with Epics

**Kevin (PO) presents:**
```
Epic #1: File Upload & Validation (26 pts)
├── Sprint 1: Stories #11, #12, #14 (18 pts)
└── Sprint 2: Story #13 (13 pts)

Epic #2: Reporting & Analytics (16 pts)
└── Sprint 2: Stories #21, #22 (16 pts)
```

**Team discusses:**
- Can we complete Epic #1 in Sprint 1? No, too large
- Split across Sprint 1 and 2
- Epic #2 starts in Sprint 2 after Epic #1 core features done

### During Sprint

**Daily standup:**
```
Joseph: Working on Epic #1, Story #11, Task #11.2 (CSV parser)
Diane: Working on Epic #3, Story #31, Task #31.1 (JWT auth)
```

**Epic status visible on board:**
```
Epic #1: File Upload & Validation
├── Story #11: In Review ✓
├── Story #12: In Progress →
├── Story #13: To Do
└── Story #14: To Do
```

### Sprint Review

**Demo by Epic:**
```
Epic #1 Demo:
✓ CSV file upload working
✓ JSON file upload working
✗ Validation rules (deferred to Sprint 2)
✓ Quality score calculation working

Epic #1 Status: 75% complete (3/4 stories done)
```

## Best Practices

### For Product Owners
- Create epics during product backlog refinement
- Keep epics focused on single feature area
- Update epic progress regularly
- Close epic only when ALL stories are done

### For Developers
- Reference epic number in commits: `feat(epic-1): add CSV parser`
- Update epic checklist when story is completed
- Coordinate with team members on same epic

### For Scrum Masters
- Track epic progress across sprints
- Identify epic blockers early
- Ensure epic goals align with sprint goals

## Example: Complete Epic Lifecycle

### Week 1: Epic Created
```
Kevin creates Epic #1: File Upload & Validation
- 4 user stories identified
- 26 story points estimated
- Spans 2 sprints
```

### Week 2: Sprint 1 Planning
```
Team commits to 3 stories from Epic #1:
- Story #11: CSV Upload (8 pts)
- Story #12: JSON Upload (5 pts)
- Story #14: Quality Score (5 pts)
Total: 18 pts
```

### Week 2-3: Sprint 1 Development
```
Day 1: Stories broken into tasks
Day 2-3: Development and testing
Day 4: Demo - 3 stories complete
Epic #1: 75% done
```

### Week 4: Sprint 2 Planning
```
Team commits to remaining story:
- Story #13: Validation Rules (13 pts)
Plus Epic #2 stories
```

### Week 4-5: Sprint 2 Development
```
Day 4: Story #13 complete
Epic #1: 100% done ✓
Kevin closes Epic #1
```

## Quick Reference

### Create Epic
```
GitHub → Issues → New Issue → Epic template
Title: [EPIC] Feature name
Label: type: epic
```

### Link Story to Epic
```
In story description:
Part of #[epic-number]
```

### Track Epic Progress
```
Option 1: Milestone
Option 2: Label filter
Option 3: Manual checklist in epic description
```

### Close Epic
```
When ALL user stories are:
- Completed
- Tested
- Deployed
- PO approved
```

---

**Remember:** Epics help organize large features. Use them to track multi-sprint initiatives and coordinate team efforts!
