# MWECAU ICT Club Portal

<div align="center">

![MWECAU ICT Club](https://img.shields.io/badge/MWECAU-ICT%20Club-blue?style=for-the-badge&logo=university&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)

**A comprehensive Django-based platform serving as both a public portfolio and member management system for the Mwenge Catholic University ICT Club.**

[Features](#features) • [Tech Stack](#tech-stack) • [Installation](#installation) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

## Features

### Public Website
- **About ICT Club** - Mission, vision, and history
- **Six Departments** - Overview of all technical departments
- **Project Portfolio** - Showcase with GitHub integration
- **Events & Announcements** - Stay updated with club activities
- **Contact System** - Form with email notifications
- **Social Integration** - Connect through social media

### Member Portal
- **Smart Registration** - Unique registration number validation
- **Approval Workflow** - Two-tier approval system (Admin + Department Leader)
- **Profile Management** - Picture upload with Cloudinary integration
- **72-Hour Enforcement** - Mandatory profile picture upload
- **Personal Dashboard** - Track your membership journey
- **Email Notifications** - Stay informed of all actions

### Leadership Dashboard
- **Member Management** - Oversee department members
- **Approval System** - Review and approve/reject registrations
- **Department Analytics** - Track statistics and growth
- **Bulk Communications** - Email notifications to members

### Admin Dashboard
- **Full System Control** - Complete platform administration
- **Database Management** - Member and department oversight
- **Content Management** - Announcements, events, and projects
- **Email Administration** - Manage all communications

---

## Tech Stack

### Backend & Framework
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-Server-499848?style=for-the-badge&logo=gunicorn&logoColor=white)

### Database
![SQLite](https://img.shields.io/badge/SQLite-Development-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Production-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Alternative-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

### Cloud & Services
![Cloudinary](https://img.shields.io/badge/Cloudinary-Image%20Storage-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail-SMTP-EA4335?style=for-the-badge&logo=gmail&logoColor=white)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap_5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### Development Tools
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

## Project Structure

```
mwecau_ict/
├── 📂 src/                        # Django project root
│   ├── 📂 config/                 # Project configuration
│   │   ├── settings.py            # Main settings
│   │   ├── urls.py                # URL routing
│   │   ├── wsgi.py                # WSGI configuration
│   │   └── asgi.py                # ASGI configuration
│   │
│   ├── 📂 accounts/               # User & authentication
│   │   ├── models.py              # User models
│   │   ├── views.py               # Authentication views
│   │   ├── forms.py               # Registration forms
│   │   ├── admin.py               # Admin interface
│   │   ├── decorators.py          # Custom decorators
│   │   ├── middleware.py          # Picture enforcement
│   │   └── email_utils.py         # Email utilities
│   │
│   ├── 📂 membership/             # Payment & membership
│   │   ├── models.py              # Payment models
│   │   ├── views.py               # Payment handling
│   │   └── admin.py               # Admin interface
│   │
│   ├── 📂 core/                   # Portfolio & announcements
│   │   ├── models.py              # Content models
│   │   ├── views.py               # Public pages
│   │   └── admin.py               # Content management
│   │
│   ├── 📂 templates/              # HTML templates
│   ├── 📂 static/                 # Static files (CSS/JS)
│   └── 📂 media/                  # User uploads
│
├── 📂 docs/                       # Documentation
│   ├── 📂 guides/                 # Feature guides
│   ├── 📂 deployment/             # Deployment docs
│   └── 📄 CHANGELOG.md
│
├── 📄 README.md                   # This file
├── 📄 CONTRIBUTORS.md             # Contributors list
└── 📄 CONTRIBUTING.md             # Contribution guidelines
```

---

## Installation

### Prerequisites

- **Python** 3.10 or higher
- **pip** & **virtualenv**
- **Git**
- **SQLite** (included with Python)
- **MySQL** (for production)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/mwecauictclub/mwecau_ict.git
cd mwecau_ict

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r docs/setup/requirements.txt

# 4. Configure environment variables
cp public/.env.example scripts/.env
# Edit scripts/.env with your configuration

# 5. Run migrations
cd src
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Initialize data
python manage.py init_ict_data

# 8. Run development server
python manage.py runserver
```

Visit **http://localhost:8000** to view the application.

---

## Configuration

### Required Environment Variables

Create a `.env` file in the `scripts/` directory:

```env
# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here

# Email Configuration (Gmail SMTP)
EMAIL_HOST_USER=mwecauictclub@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Cloudinary (Production Image Storage)
USE_CLOUDINARY=False
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Gmail App Password Setup

1. Enable 2-Factor Authentication on your Google account
2. Visit [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate an app-specific password for Gmail
4. Use this password in `EMAIL_HOST_PASSWORD`

---

## Documentation

Comprehensive documentation is available in the `docs/` directory:

### Core Documentation
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture, components, and design patterns
- **[DATABASE_DESIGN.md](docs/DATABASE_DESIGN.md)** - Database schema, ER diagrams, and queries
- **[API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - REST API endpoints and usage

### Guides & Setup
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project
- **[CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md)** - Community guidelines
- **[CHANGELOG.md](docs/CHANGELOG.md)** - Version history and releases

### Feature Guides
- **[EMAIL_SYSTEM_GUIDE.md](docs/guides/EMAIL_SYSTEM_GUIDE.md)** - Email configuration
- **[EMAIL_SYSTEM_COMPLETE.md](docs/guides/EMAIL_SYSTEM_COMPLETE.md)** - Complete email documentation
- **[DOCKER_GUIDE.md](docs/setup/DOCKER_GUIDE.md)** - Docker setup and deployment

### Deployment
- **[DEPLOYMENT_READY.md](docs/deployment/DEPLOYMENT_READY.md)** - Production deployment guide
- **[DOCKER_SETUP_SUMMARY.md](docs/setup/DOCKER_SETUP_SUMMARY.md)** - Docker Compose reference

---

## Contributing

We welcome contributions from all members of the ICT Club! Whether you're a programmer, designer, writer, or organizer, there's a place for you.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Non-Code Contributions

-  Documentation improvements
-  Design and UI/UX suggestions
-  Bug reports and testing
-  Feature ideas and feedback
-  Content creation and marketing
-  Event organization

**Read our full [Contributing Guidelines](CONTRIBUTING.md) and add yourself to [CONTRIBUTORS.md](CONTRIBUTORS.md)!**

---

## Security

We take security seriously. This project implements:

- Unique registration number validation
- Email verification during registration
- Role-based access control (RBAC)
- Password hashing (Django PBKDF2)
- CSRF protection
- XSS protection
- SQL injection prevention
- Rate limiting on sensitive endpoints
- Secure image storage (Cloudinary)

**Found a security vulnerability?** Please email us at **mwecauictclub@gmail.com** instead of opening a public issue.

---

## Mobile Responsive

- Mobile-first design approach
- Responsive across all devices
- Touch-friendly interface
- Optimized performance

---

## Roadmap

- [+] Event management system
- [+] Online certificate generation (PDF)
- [+] Resource library (tutorials, notes)
- [+] Internal messaging system
- [+] AI chatbot for club information
- [+] Competition submission portal
- [+] Mobile app (React Native)
- [+] Advanced analytics dashboard

---

## Support & Contact

<div align="center">

**Email:** [mwecauictclub@gmail.com](mailto:mwecauictclub@gmail.com)

**GitHub:** [github.com/mwecauictclub](https://github.com/mwecauictclub)

**Institution:** Mwenge Catholic University, Moshi, Tanzania

</div>

---

## License

This project is proprietary to **Mwenge Catholic University ICT Club**.

All rights reserved © 2025

---

## Contributors

We appreciate all contributors who have helped make this project successful! Check out our amazing [Contributors](CONTRIBUTORS.md).

---

<div align="center">

**Made with ❤️ by MWECAU ICT Club Development Team**

![Footer](https://img.shields.io/badge/MWECAU-ICT%20Club-blue?style=for-the-badge)

**Last Updated:** December 2025

</div>
