# MWECAU ICT Club Platform - Architecture Documentation

## Table of Contents

1. Overview
2. System Architecture
3. Technology Stack
4. Directory Structure
5. Key Components
6. Database Design
7. Authentication Flow
8. API Endpoints
9. Email System Architecture
10. Security Considerations

---

## 1. Overview

The MWECAU ICT Club Platform is a web-based Django application designed to manage club memberships, departments, projects, events, and communications. The platform serves as a centralized hub for club members to register, collaborate, and stay informed about club activities.

**Key Features:**
- User authentication and registration with flexible credentials
- Department and role-based access control
- Member management with approval workflows
- Email notification system for key events
- Project and event management
- Contact message system
- Admin dashboard for leadership

---

## 2. System Architecture

### High-Level Architecture

```
    User Interface (Django Templates)
              |
              v
    Django Application Layer
    |       |       |       |
    v       v       v       v
Accounts  Core  Membership Config
  App     App      App      Module
    |       |       |       |
    +-------+-------+-------+
            |
            v
      Django ORM
            |
            v
    Database Layer
   (SQLite/PostgreSQL)
```

### Application Flow

```
1. User Registration
   Register -> Validate -> Create User -> Send Notification -> Pending Approval

2. User Authentication
   Input Credentials -> Flexible Auth Backend -> Check Password -> Grant Access

3. Department Management
   User -> Select Department -> Assign to Department -> Get Permissions

4. Member Lifecycle
   Registration -> Pending -> Approved -> Active -> Can Upload Picture

5. Notifications
   Event Triggered -> Format Email -> Send via Email Service -> Log Status
```

---

## 3. Technology Stack

### Backend
- **Framework:** Django 4.2.27
- **Python Version:** 3.8+
- **ORM:** Django ORM with SQLite (development) / PostgreSQL (production)
- **Task Queue:** Celery (optional, for async emails)
- **Web Server:** Gunicorn (production)

### Frontend
- **Template Engine:** Django Templates
- **CSS Framework:** Tailwind CSS (current migration target)
- **JavaScript:** Vanilla JS + jQuery (legacy, being phased out)
- **Forms:** Django Forms with HTML5 validation

### Database
- **Development:** SQLite
- **Production:** PostgreSQL
- **Migrations:** Django Migrations

### Authentication
- **Default:** Django Auth with custom backend
- **Custom Backend:** EmailOrRegNumberBackend
- **Password Hashing:** PBKDF2 (Django default)

### Email
- **Backend:** Django Email Backend
- **Provider:** SMTP (configured via settings)
- **Templates:** HTML with fallback text
- **Bulk Operations:** Custom management commands

### Deployment
- **Containerization:** Docker + Docker Compose
- **Web Server:** Nginx (reverse proxy)
- **Process Manager:** Gunicorn or uWSGI
- **Static Files:** Whitenoise or Nginx

---

## 4. Directory Structure

```
mwecau_ict/
├── src/
│   ├── accounts/              # User management and authentication
│   │   ├── models.py          # CustomUser, Department, Course
│   │   ├── views.py           # Registration, login, profile
│   │   ├── forms.py           # User creation and update forms
│   │   ├── backends.py        # Custom auth backend
│   │   ├── validators.py      # Field validation rules
│   │   ├── email_service.py   # Email sending logic
│   │   ├── admin.py           # Admin customization
│   │   ├── urls.py            # URL routing
│   │   ├── signals.py         # Django signals
│   │   ├── decorators.py      # Custom decorators
│   │   ├── middleware.py      # Custom middleware
│   │   ├── management/        # Management commands
│   │   │   └── commands/
│   │   │       ├── send_bulk_email.py
│   │   │       ├── test_email.py
│   │   │       └── create_superuser.py
│   │   ├── migrations/        # Database migrations
│   │   └── templatetags/      # Custom template tags
│   │
│   ├── core/                  # Core functionality
│   │   ├── models.py          # Project, Event, Announcement, ContactMessage
│   │   ├── views.py           # Public pages and listings
│   │   ├── admin.py           # Admin configuration
│   │   ├── urls.py            # URL routing
│   │   ├── utils.py           # Utility functions
│   │   ├── middleware.py      # Custom middleware
│   │   ├── migrations/        # Database migrations
│   │   └── tests.py           # Unit tests
│   │
│   ├── membership/            # Membership and payments
│   │   ├── models.py          # Placeholder for future
│   │   ├── views.py           # Payment processing
│   │   ├── admin.py           # Admin customization
│   │   ├── urls.py            # URL routing
│   │   ├── migrations/        # Database migrations
│   │   └── tests.py           # Unit tests
│   │
│   ├── static/                # Static files (CSS, JS, images)
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── forms.js
│   │   │   └── password-strength.js
│   │   └── images/
│   │
│   ├── templates/             # HTML templates
│   │   ├── base.html          # Base template
│   │   ├── 404.html           # Error pages
│   │   ├── 500.html
│   │   ├── accounts/          # User-related templates
│   │   ├── core/              # Core feature templates
│   │   ├── emails/            # Email templates
│   │   └── includes/          # Reusable template snippets
│   │
│   ├── config/                # Project configuration
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # URL configuration
│   │   ├── wsgi.py            # WSGI application
│   │   ├── asgi.py            # ASGI application
│   │   ├── celery.py          # Celery configuration
│   │   └── gunicorn.py        # Gunicorn configuration
│   │
│   ├── manage.py              # Django management
│   └── db.sqlite3             # Development database
│
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md        # This file
│   ├── DATABASE_DESIGN.md     # Database schema
│   ├── API_DOCUMENTATION.md   # API reference
│   ├── CHANGELOG.md           # Version history
│   ├── CODE_OF_CONDUCT.md     # Community guidelines
│   ├── CONTRIBUTING.md        # Contribution guide
│   ├── guides/                # Implementation guides
│   │   ├── EMAIL_SYSTEM_GUIDE.md
│   │   └── EMAIL_SYSTEM_COMPLETE.md
│   ├── deployment/            # Deployment guides
│   │   └── DEPLOYMENT_READY.md
│   ├── setup/                 # Setup guides
│   │   ├── DOCKER_GUIDE.md
│   │   ├── DOCKER_SETUP_SUMMARY.md
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── requirements.txt
│   ├── FEATURES_IMPLEMENTATION_AUDIT.md
│   └── USERS.md
│
├── public/                    # Public assets
│   ├── .env.example           # Environment template
│   └── images/                # Public images
│
├── scripts/                   # Utility scripts
│   ├── EMAIL_QUICK_REFERENCE.sh
│   └── tests_email.py
│
├── README.md                  # Project README
├── CONTRIBUTORS.md            # Contributors list
├── DIRECTORY_STRUCTURE.md     # This directory guide
├── LICENSE                    # MIT License
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
└── docker-compose.yml         # Docker Compose setup
```

---

## 5. Key Components

### 5.1 Authentication System

**Files:**
- `src/accounts/backends.py` - Custom authentication backend
- `src/accounts/models.py` - CustomUser model
- `src/accounts/forms.py` - Registration and login forms

**Features:**
- Flexible authentication: Email, Registration Number, or Username
- Password strength validation
- Case-insensitive credential matching
- Audit logging for security events

**Flow:**
```
User Input (Email/RegNum/Username + Password)
    |
    v
EmailOrRegNumberBackend.authenticate()
    |
    +-- Query User by email/reg_number/username
    |
    +-- Verify Password Hash
    |
    +-- Check if User is Active
    |
    v
Return User or None
```

### 5.2 User Registration

**Files:**
- `src/accounts/forms.py` - Registration form
- `src/accounts/views.py` - Registration view
- `src/accounts/email_service.py` - Welcome email

**Flow:**
```
Registration Form Submission
    |
    v
CustomUserCreationForm.clean() - Validate all fields
    |
    +-- Validate email uniqueness
    +-- Validate reg_number format and uniqueness
    +-- Validate password strength
    +-- Validate full_name format
    |
    v
CustomUserCreationForm.save()
    |
    +-- Create CustomUser
    +-- Set username = reg_number (normalized)
    +-- Split full_name into parts
    +-- Assign department
    |
    v
Send Welcome Email
    |
    v
Redirect to Pending Approval Page
```

### 5.3 Department Management

**Files:**
- `src/accounts/models.py` - Department model
- `src/accounts/views.py` - Department views
- `src/accounts/admin.py` - Department admin

**Features:**
- 6 predefined departments
- Department leaders with special permissions
- Role-based access control
- Member filtering by department

### 5.4 Email System

**Files:**
- `src/accounts/email_service.py` - Email service class
- `src/templates/emails/` - Email templates
- `src/accounts/management/commands/` - Email commands

**Key Classes:**
```python
class EmailService:
    send_email(to, subject, template, context)
    send_bulk_email(recipients, subject, template, context)
    send_welcome_email(user)
    send_approval_email(user)
    send_rejection_email(user, reason)
    send_staff_notification_registration(user)
    send_staff_notification_approval(user)
    send_staff_notification_rejection(user, reason)
    send_contact_reply_email(message, reply)
```

**Email Templates:**
- `registration_confirmation.html` - Welcome email
- `approval_confirmation.html` - Approval notification
- `rejection_notification.html` - Rejection notification
- `staff_notifications.html` - Admin alerts

### 5.5 Admin Dashboard

**Files:**
- `src/accounts/admin.py` - Admin customization
- `src/core/admin.py` - Core admin setup

**Features:**
- User management with approval workflow
- Department and course management
- Project and event management
- Contact message system
- Bulk email sending
- Custom filters and actions

---

## 6. Database Design

### Core Models

**CustomUser**
```
Field               Type            Notes
id                  Auto            Primary Key
username            CharField       Generated from reg_number
reg_number          CharField       Format: T/XXXX/YYYY/NNNN (unique)
first_name          CharField       From AbstractUser
last_name           CharField       From AbstractUser
surname             CharField       Optional additional name part
full_name           CharField       Complete user name
email               EmailField      Unique identifier
password            CharField       Hashed password
course              ForeignKey      Reference to Course
course_other        CharField       For unlisted courses
department          ForeignKey      Reference to Department
picture             ImageField      Profile picture
picture_uploaded_at DateTimeField   When picture was uploaded
is_approved         BooleanField    Admin approval status
is_staff            BooleanField    Admin user flag
is_superuser        BooleanField    Superuser flag
is_department_leader BooleanField   Department leader flag
is_katibu           BooleanField    Secretary flag
is_katibu_assistance BooleanField   Secretary assistant flag
registered_at       DateTimeField   Registration timestamp
approved_at         DateTimeField   Approval timestamp
last_login          DateTimeField   Last login time
is_active           BooleanField    Active account flag
```

**Department**
```
Field               Type            Notes
id                  Auto            Primary Key
name                CharField       Unique department name
slug                SlugField       URL-friendly name
description         TextField       Department description
leader              OneToOne        Reference to CustomUser
created_at          DateTimeField   Creation timestamp
updated_at          DateTimeField   Update timestamp
```

**Course**
```
Field               Type            Notes
id                  Auto            Primary Key
name                CharField       Unique course name
code                CharField       Course code
level               CharField       DEG, CERT, DIP, MASTER, PHD
```

**Project**
```
Field               Type            Notes
id                  Auto            Primary Key
title               CharField       Project title
description         TextField       Detailed description
department          ForeignKey      Department reference
leader              ForeignKey      Project lead user
status              CharField       Active, Completed, Planning
members             ManyToMany      Project team members
created_at          DateTimeField   Creation timestamp
updated_at          DateTimeField   Update timestamp
```

**Event**
```
Field               Type            Notes
id                  Auto            Primary Key
title               CharField       Event name
description         TextField       Event description
date                DateTimeField   Event date/time
location            CharField       Event location
department          ForeignKey      Organizing department
attendees           ManyToMany      Users attending
created_at          DateTimeField   Creation timestamp
updated_at          DateTimeField   Update timestamp
```

**Announcement**
```
Field               Type            Notes
id                  Auto            Primary Key
title               CharField       Announcement title
content             TextField       Full announcement text
author              ForeignKey      User who created it
department          ForeignKey      Target department
created_at          DateTimeField   Creation timestamp
updated_at          DateTimeField   Update timestamp
```

**ContactMessage**
```
Field               Type            Notes
id                  Auto            Primary Key
sender_name         CharField       User's name
sender_email        EmailField      User's email
subject             CharField       Message subject
message             TextField       Message content
responded           BooleanField    Has admin responded
response            TextField       Admin response
created_at          DateTimeField   Message timestamp
updated_at          DateTimeField   Update timestamp
```

---

## 7. Authentication Flow

### Login Flow

```
1. User visits login page
   - Form displays three input options
   - User can enter email, reg_number, or username

2. User submits credentials
   - Form validated on client-side
   - Submitted to LoginView

3. LoginView processes:
   - username field set to user input
   - password validated against CustomUser.check_password()
   - Authentication backend called

4. EmailOrRegNumberBackend.authenticate():
   - Queries: User(email=input) OR User(reg_number=input) OR User(username=input)
   - Case-insensitive matching (using __iexact)
   - Verifies password hash
   - Checks user.is_active
   - Returns User if valid, None otherwise

5. Authentication success:
   - Session created
   - User redirected to dashboard
   - Login logged to audit trail

6. Authentication failure:
   - Error message displayed
   - User redirected to login form
   - Invalid attempt logged
```

### Registration Flow

```
1. User visits registration page
   - Form displays all required fields
   - Validation rules displayed

2. User submits registration
   - Form validates on submission

3. CustomUserCreationForm validation:
   - validate_email() - Check uniqueness
   - validate_reg_number() - Format and uniqueness
   - validate_password1() - Strength requirements
   - validate_full_name() - Format check
   - clean() - Cross-field validation

4. Form save():
   - Create CustomUser instance
   - Set username = reg_number (normalized to uppercase)
   - Split full_name into first_name, last_name, surname
   - Set department from form
   - Save to database

5. Post-registration:
   - Send welcome email
   - Create approval notification for staff
   - User redirected to pending page
   - User must wait for approval

6. Admin approval:
   - Admin reviews in dashboard
   - Approves or rejects
   - Notification email sent to user
   - If approved: User can now login
```

---

## 8. API Endpoints

### Authentication Endpoints

```
POST /accounts/register/
    Description: User registration
    Parameters: reg_number, full_name, email, course, department, password1, password2
    Returns: User created, redirect to pending page
    
GET/POST /accounts/login/
    Description: User login
    Parameters: username (email/reg_number/username), password
    Returns: Session created, redirect to dashboard
    
GET /accounts/logout/
    Description: User logout
    Returns: Session destroyed, redirect to home
    
GET /accounts/profile/
    Description: View user profile
    Returns: User profile page
    
GET/POST /accounts/profile/edit/
    Description: Edit user profile
    Parameters: full_name, email, department, picture, course
    Returns: Updated profile, redirect to profile
```

### Department Endpoints

```
GET /accounts/department/<slug>/members/
    Description: List department members
    Returns: Filtered members list
    
GET /departments/
    Description: List all departments
    Returns: All departments with leaders
    
GET /departments/<slug>/
    Description: Department detail view
    Returns: Department info, projects, members
```

### Core Endpoints

```
GET /
    Description: Home page
    Returns: Homepage with announcements and projects
    
GET /about/
    Description: About page
    Returns: Club information
    
GET /faq/
    Description: FAQ page
    Returns: Frequently asked questions
    
GET /projects/
    Description: List projects
    Returns: All club projects
    
GET /projects/<id>/
    Description: Project detail
    Returns: Project info, members, updates
    
GET /events/
    Description: List events
    Returns: Upcoming and past events
    
GET /events/<id>/
    Description: Event detail
    Returns: Event info, attendees, updates
    
GET /announcements/
    Description: List announcements
    Returns: Club announcements
    
POST /contact/
    Description: Submit contact message
    Parameters: name, email, subject, message
    Returns: Confirmation page
```

---

## 9. Email System Architecture

### Email Service Class

**Location:** `src/accounts/email_service.py`

**Key Methods:**
```python
def send_email(to, subject, template_name, context):
    Sends single email using HTML template
    
def send_bulk_email(recipients, subject, template_name, context):
    Sends email to multiple recipients
    Logs failures separately
    
def send_staff_notification_registration(user):
    Alerts all staff when new user registers
    
def send_staff_notification_approval(user):
    Alerts all staff when user is approved
    
def send_staff_notification_rejection(user, reason):
    Alerts all staff when user is rejected
    
def send_contact_reply_email(message, reply):
    Sends response to contact message
```

### Email Templates

**Location:** `src/templates/emails/`

Templates include:
- HTML version (primary)
- Text fallback (for text clients)
- Context variables for personalization

**Template Examples:**
```
registration_confirmation.html
    - recipient_name
    - registration_number
    - approval_deadline
    - login_url

approval_confirmation.html
    - recipient_name
    - department_name
    - dashboard_url

staff_notification_registration.html
    - user_name
    - user_email
    - user_registration_number
    - registration_link

staff_notification_approval.html
    - user_name
    - approval_date
    - user_dashboard_link
```

### Email Configuration

**Settings:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@mwecau.ac.tz')
```

### Email Sending Flow

```
1. Event triggered (registration, approval, etc)
   
2. EmailService instantiated with event data
   
3. Template selected based on event type
   
4. Context prepared with user/event details
   
5. Email rendered:
   a) Fetch HTML template
   b) Render with context
   c) Create text fallback (optional)
   
6. Send via SMTP:
   a) Connect to email server
   b) Authenticate
   c) Send message
   d) Close connection
   
7. Log result:
   a) Success: Log timestamp and recipient
   b) Failure: Log error and retry strategy
   
8. Return status
```

---

## 10. Security Considerations

### Authentication Security

- Custom backend uses case-insensitive matching to prevent enumeration
- Password hashed using PBKDF2 (Django default)
- No passwords logged in audit trails
- Rate limiting on login attempts (via middleware)
- Session timeout configured

### Authorization Security

- Role-based access control (RBAC)
- Department-level permissions
- Staff-only views protected with @staff_required
- Leadership-only views protected with @leadership_required
- Ownership-based permissions for profile edits

### Data Protection

- CSRF protection enabled
- XSS prevention via template auto-escaping
- SQL injection prevention via ORM
- Secure password reset flow
- Profile pictures scanned for security

### Email Security

- Email addresses validated before sending
- Unsubscribe links included in bulk emails
- No sensitive data in email subject lines
- Email logs sanitized of passwords
- Sender address verified

### Database Security

- Database encrypted in production
- Backup and recovery procedures
- Access logs for admin operations
- Audit trail for user modifications
- No hardcoded credentials in code

### API Security

- HTTPS enforced in production
- API rate limiting
- CORS configuration
- Authentication required for protected endpoints
- Input validation on all endpoints

### Deployment Security

- Environment variables for secrets
- Docker container security scanning
- Nginx security headers
- Regular dependency updates
- Security patches applied promptly

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## License

This project is licensed under the MIT License - see [LICENSE](../LICENSE) file for details.

