# Branch Strategy & Protection Rules

## Branch Structure

```
main (production)
  └── develop (integration)
       ├── feature/feature-name
       ├── bugfix/bug-name
       └── hotfix/hotfix-name
```

## Branch Protection Rules

### 1. Main Branch (`main`)
- **Protected:** Yes
- **Can merge from:** `develop` ONLY
- **Cannot merge from:** feature/, bugfix/, hotfix/ branches directly
- **Requires:** PR approval, passing CI/CD
- **Purpose:** Production-ready code

### 2. Develop Branch (`develop`)
- **Protected:** Yes
- **Can merge from:** feature/, bugfix/, hotfix/ branches ONLY
- **Cannot merge from:** Any other branches
- **Requires:** PR approval, passing CI/CD
- **Purpose:** Integration and testing

### 3. Feature Branches (`feature/*`)
- **Protected:** No
- **Can merge to:** `develop` ONLY
- **Naming:** `feature/task-description`
- **Purpose:** New features and enhancements

### 4. Bugfix Branches (`bugfix/*`)
- **Protected:** No
- **Can merge to:** `develop` ONLY
- **Naming:** `bugfix/issue-description`
- **Purpose:** Bug fixes

### 5. Hotfix Branches (`hotfix/*`)
- **Protected:** No
- **Can merge to:** `main` OR `develop`
- **Naming:** `hotfix/critical-issue`
- **Purpose:** Critical production fixes that need immediate deployment

## Workflow Enforcement

### Automated Checks (via GitHub Actions)

The `.github/workflows/branch-protection.yml` workflow enforces:

1. **PRs to `develop`:**
   - ✅ Allowed: `feature/*`, `bugfix/*`, `hotfix/*`
   - ❌ Blocked: `main`, any other branches

2. **PRs to `main`:**
   - ✅ Allowed: `develop`, `hotfix/*`
   - ❌ Blocked: `feature/*`, `bugfix/*`, any other branches

### Manual GitHub Settings

Configure in GitHub Repository Settings → Branches:

#### For `main` branch:
```
☑ Require pull request reviews before merging
☑ Require status checks to pass before merging
  - CI Pipeline
  - Branch Protection
☑ Require branches to be up to date before merging
☑ Include administrators
☐ Allow force pushes
☐ Allow deletions
```

#### For `develop` branch:
```
☑ Require pull request reviews before merging
☑ Require status checks to pass before merging
  - CI Pipeline
  - Branch Protection
☑ Require branches to be up to date before merging
☑ Include administrators
☐ Allow force pushes
☐ Allow deletions
```

## Developer Workflow

### Creating a Feature
```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
# ... make changes ...
git push origin feature/my-feature
# Create PR to develop
```

### Merging to Production
```bash
# After features are tested in develop
git checkout develop
git pull origin develop
# Create PR from develop to main
```

## Common Scenarios

### ✅ Allowed Workflows

1. **Feature Development:**
   ```
   feature/upload-api → develop (via PR)
   ```

2. **Bug Fix:**
   ```
   bugfix/null-check → develop (via PR)
   ```

3. **Release to Production:**
   ```
   develop → main (via PR)
   ```

4. **Critical Hotfix:**
   ```
   hotfix/security-fix → main (via PR)
   hotfix/security-fix → develop (via PR, to keep in sync)
   ```

### ❌ Blocked Workflows

1. **Direct to Main:**
   ```
   feature/upload-api → main ❌ BLOCKED
   ```

2. **Wrong Branch to Develop:**
   ```
   main → develop ❌ BLOCKED
   random-branch → develop ❌ BLOCKED
   ```

3. **Bypass Develop:**
   ```
   feature/upload-api → main ❌ BLOCKED
   ```

## Error Messages

### When trying to merge feature to main:
```
Error: Only develop branch can merge to main
Pull request validation failed
```

### When trying to merge wrong branch to develop:
```
Error: Only feature/, bugfix/, or hotfix/ branches can merge to develop
Pull request validation failed
```

## Emergency Procedures

### Critical Hotfix Process
1. Create hotfix branch from `main`
2. Fix the critical issue
3. Merge to `main` via PR (immediate production fix)
4. Also merge to `develop` via PR (keep branches in sync)

```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix
# ... fix issue ...
git push origin hotfix/critical-security-fix
# PR to main → merge (URGENT)
# PR to develop → merge (sync)
```

## Enforcement Timeline

- **Day 1:** Configure branch protection in GitHub settings
- **Day 1:** Deploy branch-protection.yml workflow
- **Day 1:** Communicate rules to all team members
- **Ongoing:** Automated enforcement via GitHub Actions

## Team Training

All team members must:
1. Read this document
2. Understand the branch strategy
3. Follow naming conventions
4. Never force push to protected branches
5. Always create PRs for merging

## Monitoring

Scrum Master/DevOps should:
- Monitor failed PR checks
- Review branch protection violations
- Update rules as needed
- Train team members on violations
