# Database Design Documentation

## Overview

This document describes the complete database schema for the MWECAU ICT Club Platform. The database uses Django ORM with SQLite for development and PostgreSQL for production.

---

## Entity-Relationship Diagram

```
                              CustomUser
                              +--------+
                              | id (PK)|
                              | reg... |
                              | email  |
                              | ...    |
                              +--------+
                                 | | |
                    +-----------+-+-+-----------+
                    |           |   |           |
                    v           v   v           v
              Department     Course  Project  Event
              (Leader FK)    (FK)  (Leader FK)(FK)
                |             |      |         |
                |             |      |         |
            Members(1:M)  Members(1:M)|    Attendees(M:M)
                |             |      |         |
                |             |      v         |
                |             |   Project      |
                |             |   Members(M:M) |
                |             |      |         |
                |             |      v         |
                |             |   CustomUser   |
                |             |      |         |
                |             +------+---------+
                |                    |
                +--------------------+
                        |
                   CustomUser
```

---

## Table Definitions

### 1. CustomUser Table

Custom user model extending Django's AbstractUser with club-specific fields.

**Table Name:** `accounts_customuser`

**Columns:**

| Column Name | Type | Constraints | Notes |
|------------|------|-------------|-------|
| id | BigAutoField | PRIMARY KEY | Auto-generated ID |
| password | CharField(128) | NOT NULL | Hashed password |
| last_login | DateTimeField | NULL | Last login timestamp |
| is_superuser | BooleanField | NOT NULL, DEFAULT=False | Admin flag |
| username | CharField(150) | UNIQUE, NOT NULL | Login username |
| first_name | CharField(150) | NOT NULL | User's first name |
| last_name | CharField(150) | NOT NULL | User's last name |
| email | EmailField(254) | UNIQUE, NOT NULL | User's email |
| is_staff | BooleanField | NOT NULL, DEFAULT=False | Staff member flag |
| is_active | BooleanField | NOT NULL, DEFAULT=True | Account active flag |
| date_joined | DateTimeField | NOT NULL | Account creation date |
| reg_number | CharField(20) | UNIQUE, NOT NULL | Registration number |
| surname | CharField(100) | NOT NULL | Optional surname |
| full_name | CharField(200) | NOT NULL | Complete name |
| course_id | BigIntegerField | FOREIGN KEY | Reference to Course |
| course_other | CharField(150) | NOT NULL | For unlisted courses |
| department_id | BigIntegerField | FOREIGN KEY | Reference to Department |
| is_approved | BooleanField | NOT NULL, DEFAULT=False | Admin approval |
| picture | ImageField | NULL | Profile picture path |
| picture_uploaded_at | DateTimeField | NULL | When picture uploaded |
| registered_at | DateTimeField | NOT NULL | Registration timestamp |
| approved_at | DateTimeField | NULL | Approval timestamp |
| is_department_leader | BooleanField | NOT NULL, DEFAULT=False | Leader flag |
| is_katibu | BooleanField | NOT NULL, DEFAULT=False | Secretary flag |
| is_katibu_assistance | BooleanField | NOT NULL, DEFAULT=False | Secretary asst flag |

**Indexes:**
```
CREATE INDEX idx_reg_number ON accounts_customuser(reg_number);
CREATE INDEX idx_email ON accounts_customuser(email);
CREATE INDEX idx_username ON accounts_customuser(username);
CREATE INDEX idx_is_approved_registered ON accounts_customuser(is_approved, registered_at);
```

**Unique Constraints:**
```
UNIQUE(username)
UNIQUE(email)
UNIQUE(reg_number)
```

**Sample Data:**
```
id: 1
username: T/DEG/2025/001
reg_number: T/DEG/2025/001
first_name: John
last_name: Doe
surname: Smith
full_name: John Doe Smith
email: john.doe@mwecau.ac.tz
is_approved: True
department_id: 1
course_id: 1
is_active: True
registered_at: 2025-12-15 10:30:00
approved_at: 2025-12-15 14:45:00
```

---

### 2. Department Table

Represents the six departments in the ICT Club.

**Table Name:** `accounts_department`

**Columns:**

| Column Name | Type | Constraints | Notes |
|------------|------|-------------|-------|
| id | BigAutoField | PRIMARY KEY | Auto-generated ID |
| name | CharField(100) | UNIQUE, NOT NULL | Department name |
| slug | SlugField(50) | UNIQUE, NOT NULL | URL-friendly slug |
| description | TextField | NOT NULL | Department description |
| leader_id | BigIntegerField | FOREIGN KEY, NULL | Department leader |
| created_at | DateTimeField | NOT NULL | Creation date |
| updated_at | DateTimeField | NOT NULL | Last update |

**Indexes:**
```
CREATE INDEX idx_slug ON accounts_department(slug);
CREATE INDEX idx_name ON accounts_department(name);
```

**Predefined Departments:**
```
1. Programming (slug: programming)
2. Cybersecurity (slug: cybersecurity)
3. Networking (slug: networking)
4. Computer Maintenance (slug: maintenance)
5. Graphic Design (slug: design)
6. AI & Machine Learning (slug: ai_ml)
```

**Foreign Keys:**
```
leader_id -> accounts_customuser(id) ON DELETE SET_NULL
```

---

### 3. Course Table

Represents available courses at MWECAU.

**Table Name:** `accounts_course`

**Columns:**

| Column Name | Type | Constraints | Notes |
|------------|------|-------------|-------|
| id | BigAutoField | PRIMARY KEY | Auto-generated ID |
| name | CharField(150) | UNIQUE, NOT NULL | Course name |
| code | CharField(20) | NOT NULL | Course code |
| level | CharField(20) | NOT NULL | Education level |

**Course Levels:**
```
DIP: Diploma
CERT: Certificate
DEG: Bachelor Degree
MASTER: Master Degree
PHD: Doctor of Philosophy
```

**Indexes:**
```
CREATE INDEX idx_level_name ON accounts_course(level, name);
```

---

### 4. Project Table

Represents club projects.

**Table Name:** `core_project`

**Columns:**

| Column Name | Type | Constraints | Notes |
|------------|------|-------------|-------|
| id | BigAutoField | PRIMARY KEY | Auto-generated ID |
| title | CharField(200) | NOT NULL | Project title |
| description | TextField | NOT NULL | Project description |
| status | CharField(20) | NOT NULL, DEFAULT='active' | Project status |
| department_id | BigIntegerField | FOREIGN KEY, NOT NULL | Department reference |
| leader_id | BigIntegerField | FOREIGN KEY, NOT NULL | Project lead |
| created_at | DateTimeField | NOT NULL | Creation date |
| updated_at | DateTimeField | NOT NULL | Last update |

**Foreign Keys:**
```
department_id -> accounts_department(id) ON DELETE PROTECT
leader_id -> accounts_customuser(id) ON DELETE PROTECT
```

**Many-to-Many Relationships:**
```
project_members (through table):
  - project_id -> core_project(id)
  - customuser_id -> accounts_customuser(id)
```

---

### 5. Event Table

Represents club events and activities.

**Table Name:** `core_event`

**Columns:**

| Column Name | Type | Constraints | Notes |
|------------|------|-------------|-------|
| id | BigAutoField | PRIMARY KEY | Auto-generated ID |
| title | CharField(200) | NOT NULL | Event title |
| description | TextField | NOT NULL | Event description |
| date | DateTimeField | NOT NULL | Event date/time |
| location | CharField(255) | NOT NULL | Event location |
| department_id | BigIntegerField | FOREIGN KEY, NOT NULL | Organizing dept |
| created_at | DateTimeField | NOT NULL | Creation date |
| updated_at | DateTimeField | NOT NULL | Last update |

**Foreign Keys:**
```
department_id -> accounts_department(id) ON DELETE PROTECT
```

**Many-to-Many Relationships:**
```
event_attendees (through table):
  - event_id -> core_event(id)
  - customuser_id -> accounts_customuser(id)
```

**Indexes:**
```
CREATE INDEX idx_date ON core_event(date);
CREATE INDEX idx_department ON core_event(department_id);
```

---

### 6. Announcement Table

Represents club announcements.

**Table Name:** `core_announcement`

**Columns:**

| Column Name | Type | Constraints | Notes |
|------------|------|-------------|-------|
| id | BigAutoField | PRIMARY KEY | Auto-generated ID |
| title | CharField(200) | NOT NULL | Announcement title |
| content | TextField | NOT NULL | Full content |
| author_id | BigIntegerField | FOREIGN KEY, NOT NULL | Author reference |
| department_id | BigIntegerField | FOREIGN KEY, NULL | Target department |
| created_at | DateTimeField | NOT NULL | Creation date |
| updated_at | DateTimeField | NOT NULL | Last update |

**Foreign Keys:**
```
author_id -> accounts_customuser(id) ON DELETE PROTECT
department_id -> accounts_department(id) ON DELETE SET_NULL
```

**Indexes:**
```
CREATE INDEX idx_created ON core_announcement(created_at DESC);
CREATE INDEX idx_department ON core_announcement(department_id);
```

---

### 7. ContactMessage Table

Represents contact form submissions.

**Table Name:** `core_contactmessage`

**Columns:**

| Column Name | Type | Constraints | Notes |
|------------|------|-------------|-------|
| id | BigAutoField | PRIMARY KEY | Auto-generated ID |
| sender_name | CharField(100) | NOT NULL | Sender's name |
| sender_email | EmailField(254) | NOT NULL | Sender's email |
| subject | CharField(200) | NOT NULL | Message subject |
| message | TextField | NOT NULL | Message content |
| responded | BooleanField | NOT NULL, DEFAULT=False | Response status |
| response | TextField | NULL | Admin response |
| created_at | DateTimeField | NOT NULL | Submission date |
| updated_at | DateTimeField | NOT NULL | Last update |

**Indexes:**
```
CREATE INDEX idx_created ON core_contactmessage(created_at DESC);
CREATE INDEX idx_responded ON core_contactmessage(responded);
```

---

## Relationships Summary

### One-to-Many (1:M)

| Parent | Child | Relationship |
|--------|-------|--------------|
| Department | CustomUser | Members of department |
| Department | Project | Projects in department |
| Department | Event | Events organized by |
| Department | Announcement | Announcements for dept |
| Department | Department | Department leader |
| Course | CustomUser | Members of course |
| CustomUser | Project | Projects led by |
| CustomUser | Event | Events as organizer |
| CustomUser | Announcement | Announcements authored |

### Many-to-Many (M:M)

| Table A | Table B | Junction Table |
|---------|---------|----------------|
| Project | CustomUser | core_project_members |
| Event | CustomUser | core_event_attendees |

---

## Migration Strategy

### Initial Setup

```python
# 0001_initial.py
- Create CustomUser, Department, Course
- Set up indexes and constraints

# 0002_remove_payment_type
- Remove unused payment models from membership app

# 0003_customuser_surname
- Add surname field to CustomUser

# 0004_alter_customuser_department
- Alter department field constraints
```

### Running Migrations

```bash
python manage.py makemigrations
python manage.py migrate

# Specific app
python manage.py migrate accounts
python manage.py migrate core
python manage.py migrate membership
```

---

## Query Optimization

### Common Queries

**Get user with all related data:**
```python
User.objects.select_related('department', 'course').get(id=user_id)
```

**Get department with member count:**
```python
Department.objects.annotate(
    member_count=Count('members')
).all()
```

**Get project with members:**
```python
Project.objects.prefetch_related('members').get(id=project_id)
```

**Get events for user:**
```python
user.event_set.select_related('department').all()
```

### Indexes for Performance

```sql
CREATE INDEX idx_accounts_customuser_reg_number 
  ON accounts_customuser(reg_number);

CREATE INDEX idx_accounts_customuser_email 
  ON accounts_customuser(email);

CREATE INDEX idx_accounts_customuser_is_approved_registered 
  ON accounts_customuser(is_approved, registered_at);

CREATE INDEX idx_accounts_department_slug 
  ON accounts_department(slug);

CREATE INDEX idx_core_event_date 
  ON core_event(date);

CREATE INDEX idx_core_announcement_created 
  ON core_announcement(created_at DESC);
```

---

## Data Integrity Rules

### CustomUser

- `reg_number` must match pattern: `T/(DEG|CERT|DIP|MASTER|PHD)/YYYY/NNNN`
- `username` auto-generated from `reg_number`
- `email` must be unique and valid
- `full_name` required, minimum 2 parts
- If `course` is NULL, `course_other` must be filled
- `picture` should be image file (PNG, JPG, GIF)
- `is_approved` set by admin only
- `is_active` must be True for login
- `registered_at` auto-set on creation
- `approved_at` only set when approved

### Department

- `name` and `slug` must be unique
- `leader_id` must be a valid CustomUser (if set)
- Only one leader per department
- Leader must be is_staff or is_department_leader

### Course

- `name` must be unique
- `level` must be one of predefined levels
- At least one course per level should exist

### Project

- `department_id` and `leader_id` required
- `leader_id` must be staff or department leader
- `status` must be valid choice
- Only staff can create/edit projects

### Event

- `date` should be in the future
- `department_id` required
- Email notifications sent to attendees

### Announcement

- `author_id` must be staff
- `content` can be empty (draft)
- Visible to all if `department_id` is NULL
- Otherwise visible only to department members

### ContactMessage

- `sender_email` must be valid
- `message` required, min 10 characters
- `responded` auto-set when response added
- Response email sent to sender

---

## Backup and Recovery

### Backup Strategy

```bash
# SQLite development backup
cp src/db.sqlite3 backups/db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)

# PostgreSQL production backup
pg_dump -h localhost -U postgres -d mwecau_ict > backup.sql
```

### Restore Procedure

```bash
# SQLite
cp backups/db.sqlite3.backup.20251215_100000 src/db.sqlite3

# PostgreSQL
psql -h localhost -U postgres -d mwecau_ict < backup.sql
```

---

## Database Configuration

### Development (SQLite)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'src' / 'db.sqlite3',
    }
}
```

### Production (PostgreSQL)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'mwecau_ict'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 600,
    }
}
```

---

## Performance Considerations

### Query Performance

- Use `select_related()` for foreign keys
- Use `prefetch_related()` for many-to-many
- Use `only()` or `values()` to limit fields
- Add database indexes for frequently queried fields

### Data Archival

- Archive old events after 1 year
- Archive old contact messages after 6 months
- Implement soft deletes for historical tracking
- Regular database optimization (VACUUM, ANALYZE)

### Caching Strategy

- Cache department list (changes rarely)
- Cache course list (changes rarely)
- Cache user permissions for session
- Cache announcements (1-hour TTL)

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development guidelines

