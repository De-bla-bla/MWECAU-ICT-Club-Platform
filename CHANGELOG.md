# Changelog

All notable changes to the MWECAU ICT Club Platform are documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

---

## Unreleased

### Added
- MIT License for open-source distribution
- License reference in README

### Planned Features
- REST API for third-party integrations
- Mobile app (React Native)
- Advanced analytics dashboard
- Messaging system between members
- Event livestreaming capability
- Certificate generation (PDF)
- Merchandise store integration
- AI chatbot for member support

---

## Version 1.2.0 - December 13, 2025

### Added
- Docker configuration with complete orchestration (PostgreSQL, Redis, Celery, Celery Beat)
- Docker Compose setup with 5 containerized services
- Health checks for all services with automatic recovery
- Comprehensive Docker documentation (DOCKER_GUIDE.md, DOCKER_SETUP_SUMMARY.md)
- Dual database support: SQLite (development) and PostgreSQL (production)
- Environment auto-detection for database configuration
- Code of Conduct and Contributing guidelines
- Changelog documentation
- Features Implementation Audit document
- Deployment Readiness documentation

### Fixed
- Email template None error with defensive validation
- Email service template parameter handling
- Django settings to support multiple databases
- Removed unnecessary payment-related documentation

### Changed
- README: Removed all emojis for professional documentation
- README: Honest API status (no REST API, server-side rendered)
- Technology Stack: Updated to reflect actual technologies
- Restructured documentation for clarity and maintainability
- Updated docker-compose.yml with proper service names and networking

### Improved
- Email service error handling and logging
- Gunicorn configuration with 4 workers
- Docker image optimization with slim base image
- Network architecture for service communication
- Volume management for persistent data
- Celery integration with Redis

---

## Version 1.1.0 - December 10, 2025

### Added
- Comprehensive email system refactor
- EmailService class with error handling and logging
- Management commands: send_bulk_email and test_email
- Email configuration testing capability
- Bulk email notifications with batch processing
- Picture reminder email functionality
- Email logging and error tracking
- Backward compatibility wrappers for email functions

### Fixed
- Picture upload deadline calculation
- Department members filtering
- Profile edit form validation
- Footer simplification
- JavaScript file organization
- Error page templates (404, 500)

### Changed
- Refactored email sending to centralized service
- Updated admin interface for picture reminders
- Reorganized navigation structure

### Removed
- All payment-related code and models
- M-Pesa webhook handler
- Stripe webhook handler
- Payment tracking views
- PaymentWebhookLog model
- MembershipPayment model

---

## Version 1.0.0 - November 2025

### Added
- User registration with unique registration number validation
- Approval workflow for new members (Admin + Department Leaders)
- Profile picture upload with Cloudinary integration
- 72-hour picture upload deadline enforcement
- Member dashboard with profile information
- Department member listing
- Leadership dashboard with member management
- Admin dashboard with full system administration
- Content management (announcements, events, projects)
- Contact form with email notifications
- Email notifications for all user actions
- Six departments overview
- Projects portfolio
- Events and announcements listing
- Custom Django admin interface
- Bootstrap 5 responsive design
- Role-based access control (RBAC)
- Session management
- Password change functionality
- Social media links

### Features by Module

#### Accounts App
- Custom user model with extended fields
- Registration form with validation
- Login/logout functionality
- Profile view and edit
- Picture upload with deadline
- Department assignment
- Course selection
- Approval workflow
- User status tracking

#### Core App
- Project model and listing
- Event model and calendar
- Announcement model with types
- Contact form handling
- Public pages (About, FAQs, Privacy Policy, Terms)
- Department details view

#### Membership App
- Member management
- Department statistics
- Bulk email notifications
- Leadership capabilities

#### Configuration
- Multi-app Django project structure
- Settings management with environment variables
- Static file handling
- Media file uploads
- Email configuration
- Cloudinary integration

---

## Version 0.9.0 - October 2025

### Initial Development
- Project initialization
- Django project setup
- Database models creation
- Basic views and templates
- User authentication system
- Form handling and validation
- Template inheritance setup
- CSS framework integration
- JavaScript interactions

---

## Contributors

### Lead Developer
- Clever Godson (@cleven12) - Project architect, full-stack development

### Contributors
- Community contributions welcome

---

## Versioning

This project follows Semantic Versioning:

- MAJOR version for incompatible API changes
- MINOR version for functionality additions (backward compatible)
- PATCH version for bug fixes

---

## Release Schedule

- Version 1.2.0: December 13, 2025
- Version 1.1.0: December 10, 2025
- Version 1.0.0: November 2025
- Version 0.9.0: October 2025

---

## Upgrading

### From Version 1.1.0 to 1.2.0

1. Update environment variables:
   ```bash
   cp .env.docker .env
   # Update with your configuration
   ```

2. Update requirements (if new packages added):
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Optional: Switch to Docker:
   ```bash
   docker-compose build
   docker-compose up
   ```

### From Version 1.0.0 to 1.1.0

1. No breaking changes
2. Update code: `git pull`
3. Install new dependencies: `pip install -r requirements.txt`
4. No migrations needed
5. New management commands available: test_email, send_bulk_email

---

## Known Issues

None currently reported.

---

## Support

For issues, questions, or suggestions:
- Email: mwecauictclub@gmail.com
- GitHub Issues: https://github.com/mwecauictclub/mwecau_ict/issues

---

## License

Copyright 2025 Mwenge Catholic University ICT Club. All rights reserved.

---

**Last Updated:** December 13, 2025  
**Maintained By:** ICT Club Development Team
