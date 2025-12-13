# MWECAU ICT Club Website

A comprehensive Django-based platform serving as both a public portfolio and member management system for the Mwenge Catholic University ICT Club.

**Live Repository:** https://github.com/mwecauictclub

---

## Table of Contents

1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running Locally](#running-locally)
7. [Database](#database)
8. [Deployment](#deployment)
9. [Contributing](#contributing)

---

## Features

### Public Website
- About ICT Club (mission, vision, history)
- Six departments overview
- Projects portfolio (GitHub integration)
- Events & announcements
- Contact form with email notifications
- Social media links

### Member Portal
- User registration with unique registration number validation
- Approval workflow (Admin + Department Leader)
- Profile picture upload (Cloudinary integration)
- 72-hour picture upload enforcement
- Personal dashboard
- Department information
- Email notifications for all actions

### Leadership Dashboard
- Member management
- Approval/rejection of registrations
- Department statistics
- Bulk email notifications to members

### Admin Dashboard
- Full system administration
- Member database management
- Department & leader management
- Content management (announcements, events, projects)
- Email management

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 4.2.x |
| **Web Server** | Gunicorn (Production) / Django Dev Server |
| **Database** | SQLite (Dev) / PostgreSQL (Production) |
| **Image Storage** | Cloudinary |
| **Email Service** | Gmail SMTP |
| **Frontend** | HTML5 + Bootstrap 5 + JavaScript |
| **Async Tasks** | Redis + Celery (Optional) |
| **Deployment** | Docker + Docker Compose / Traditional VPS |
| **Version Control** | Git / GitHub |

---

## Project Structure

```
mwecau_ict/
├── src/                          # Django project root
│   ├── config/                   # Project settings
│   │   ├── settings.py           # Main settings
│   │   ├── urls.py               # URL routing
│   │   ├── wsgi.py               # WSGI config
│   │   └── asgi.py               # ASGI config
│   │
│   ├── accounts/                 # User & authentication app
│   │   ├── models.py             # CustomUser, Department, Course
│   │   ├── views.py              # Registration, login, profile
│   │   ├── forms.py              # Registration & profile forms
│   │   ├── admin.py              # Admin interface
│   │   ├── decorators.py         # Custom decorators
│   │   ├── middleware.py         # Picture enforcement middleware
│   │   ├── email_utils.py        # Email utilities
│   │   └── management/           # Management commands
│   │       └── commands/
│   │           └── init_ict_data.py  # Initialize data
│   │
│   ├── membership/               # Payment & membership app
│   │   ├── models.py             # MembershipPayment, PaymentWebhookLog
│   │   ├── views.py              # Payment handling
│   │   ├── admin.py              # Admin interface
│   │   └── webhooks.py           # Payment webhooks (M-Pesa, Stripe)
│   │
│   ├── core/                     # Portfolio & announcements app
│   │   ├── models.py             # Project, Event, Announcement
│   │   ├── views.py              # Public pages
│   │   └── admin.py              # Admin interface
│   │
│   ├── templates/                # HTML templates
│   │   ├── base.html             # Base template
│   │   ├── accounts/             # Auth templates
│   │   ├── core/                 # Public templates
│   │   ├── emails/               # Email templates
│   │   └── admin/                # Custom admin templates
│   │
│   ├── static/                   # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── media/                    # User uploads
│   │   └── profile_pictures/
│   │
│   └── manage.py                 # Django management script
│
├── .env                          # Environment variables (create from .env.example)
├── .env.example                  # Environment variables template
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── docker-compose.yml            # Docker setup (optional)
```

---

## Installation

### Prerequisites

- Python 3.10+
- pip & virtualenv
- Git
- PostgreSQL (for production)
- Redis (optional, for caching/queuing)

### Step 1: Clone Repository

```bash
git clone https://github.com/mwecauictclub/mwecau_ict.git
cd mwecau_ict
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
nano .env
```

### Step 5: Run Migrations

```bash
cd src
python manage.py migrate
```

### Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 7: Initialize Data (Departments & Courses)

```bash
python manage.py init_ict_data
```

---

## Configuration

### Required Environment Variables

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here

# Email Configuration (Gmail SMTP)
EMAIL_HOST_USER=mwecauictclub@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Use App Password, not regular password

# Cloudinary (for production image storage)
USE_CLOUDINARY=False  # Set to True for production
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Gmail App Password Setup

1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app-specific password for Gmail
4. Use this password in `EMAIL_HOST_PASSWORD`

### Cloudinary Setup (Production)

1. Sign up at https://cloudinary.com
2. Get your API credentials
3. Add to `.env`:
   ```
   USE_CLOUDINARY=True
   CLOUDINARY_CLOUD_NAME=...
   CLOUDINARY_API_KEY=...
   CLOUDINARY_API_SECRET=...
   ```

---

## Running Locally

### Start Django Development Server

```bash
cd src
python manage.py runserver
```

Access at: http://localhost:8000

### Admin Interface

URL: http://localhost:8000/admin  
Username/Password: Use the superuser credentials you created

### Test Registration

1. Visit http://localhost:8000/register/
2. Fill the registration form
3. Check the admin panel for pending approvals
4. Approve from admin: http://localhost:8000/admin/accounts/customuser/

---

## Database

### Development (SQLite)

SQLite is configured by default. Database file: `src/db.sqlite3`

### Production (PostgreSQL)

Update `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ictclub',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Or use environment variables:

```bash
DB_NAME=ictclub
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Deployment

### Option 1: Heroku Deployment

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login to Heroku
heroku login

# Create app
heroku create mwecau-ict

# Add PostgreSQL add-on
heroku addons:create heroku-postgresql:hobby-dev

# Configure environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
# ... set other env vars

# Deploy
git push heroku main

# Run migrations
heroku run python src/manage.py migrate
```

### Option 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Option 3: Traditional VPS (Ubuntu)

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv postgresql nginx

# Clone and setup
git clone https://github.com/mwecauictclub/mwecau_ict.git
cd mwecau_ict
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Gunicorn
pip install gunicorn
gunicorn src.config.wsgi:application --bind 0.0.0.0:8000

# Configure Nginx (reverse proxy)
# ... (see deployment guide)
```

---

## API Status

This project is a server-side rendered Django application and does not provide a REST API. All functionality is accessed through the web interface using traditional form submissions and page redirects.

Future versions may include a REST API if needed. Currently, the project prioritizes:
- User-friendly web interface
- Server-side template rendering
- Form-based interactions
- Email notifications for all actions

---

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to contribute to this project.

---

## Email Templates

Email templates should be created in `src/templates/emails/`:

- `registration_confirmation.html` - Confirmation for new registrations
- `member_approved.html` - Approval notification
- `member_rejected.html` - Rejection notification
- `picture_reminder.html` - Picture upload reminder
- `new_registration_admin.html` - New registration alert for admins
- `new_registration_leader.html` - New registration alert for department leaders

---

## Security Measures

This project implements multiple security measures:

- Unique registration number validation
- Email verification during registration
- Role-based access control (RBAC)
- Password hashing (Django's PBKDF2)
- CSRF protection
- XSS protection
- SQL injection prevention (Django ORM)
- Rate limiting on sensitive endpoints
- Secure image URLs (Cloudinary)
- HTTPS enforcement in production  

---

## Mobile Responsiveness

- Designed with TailwindCSS for mobile-first approach
- Responsive breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Touch-friendly buttons and forms
- Optimized images for different screen sizes

---

## Troubleshooting

### Email Not Sending

1. Check `.env` for correct email credentials
2. Verify Gmail App Password (not regular password)
3. Check email logs: `python manage.py shell`
4. Enable "Less secure app access" if using regular password

### Migration Issues

```bash
# Reset migrations (development only!)
python manage.py migrate accounts zero
python manage.py migrate membership zero
python manage.py migrate core zero
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading in Production

```bash
python manage.py collectstatic --noinput
```

### Cloudinary Images Not Working

1. Check `USE_CLOUDINARY=True` in `.env`
2. Verify API credentials
3. Check image permissions in Cloudinary dashboard

---

## Support & Contact

**Email:** mwecauictclub@gmail.com  
**GitHub:** https://github.com/mwecauictclub  
**Institution:** Mwenge Catholic University, Moshi, Tanzania

---

## License

This project is proprietary to Mwenge Catholic University ICT Club.  
All rights reserved © 2025

---

## Future Enhancements

- Event management system
- Online certificate generation (PDF)
- Resource library (tutorials, notes)
- Internal messaging system
- AI chatbot for club information
- Competition submission portal
- Club merchandise store
- Mobile app (React Native)
- Live streaming for events
- Advanced analytics dashboard

---

**Last Updated:** December 2025  
**Maintained By:** ICT Club Development Team
