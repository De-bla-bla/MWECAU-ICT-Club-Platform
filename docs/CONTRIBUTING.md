# Contributing to MWECAU ICT Club Platform

Thank you for your interest in contributing to the MWECAU ICT Club Platform! This document provides guidelines for participating in the project.

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Virtual environment tool
- Text editor or IDE

### Setup Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/mwecau_ict.git
   cd mwecau_ict
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Copy environment file:
   ```bash
   cp .env.example .env
   ```

6. Run migrations:
   ```bash
   cd src
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Start development server:
   ```bash
   python manage.py runserver
   ```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please search the issue tracker to avoid duplicates. When creating a bug report, include:

- Clear title and description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Python and Django versions
- Operating system

### Suggesting Enhancements

Enhancement suggestions are welcome! When suggesting features:

- Use a clear, descriptive title
- Explain the use case and benefits
- Provide examples or mockups
- List any related features
- Explain how it differs from similar features

### Pull Requests

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the style guide
3. Add or update tests for your changes
4. Update documentation as needed
5. Commit with clear messages:
   ```bash
   git commit -m "feat: Add feature description"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Open a Pull Request with:
   - Clear title and description
   - Reference to related issues
   - Explanation of changes
   - Any breaking changes

## Coding Standards

### Python Style

Follow PEP 8 with these guidelines:

- Line length: 88 characters (Black formatter)
- Use meaningful variable and function names
- Write docstrings for classes and functions
- Use type hints where applicable

Example:
```python
def send_email(recipient: str, subject: str, message: str) -> bool:
    """
    Send an email to the specified recipient.
    
    Args:
        recipient: Email address of recipient
        subject: Email subject line
        message: Email message body
        
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Implementation
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False
```

### HTML/Template Style

- Use Bootstrap 5 classes
- Write semantic HTML
- Add alt text to images
- Test responsiveness
- Use template inheritance

### JavaScript Style

- Use meaningful variable names
- Add comments for complex logic
- Test across browsers
- Avoid inline styles

### Database

- Write proper migrations for any model changes
- Include data migrations if needed
- Test migrations up and down
- Use descriptive migration names

## Branch Naming Convention

Use these prefixes for branches:

- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions
- `chore/` - Maintenance tasks

Example:
```
feature/bulk-email-system
bugfix/picture-upload-error
docs/update-readme
refactor/simplify-email-service
```

## Commit Message Convention

Follow the Conventional Commits specification:

```
<type>: <description>

<body>

<footer>
```

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style (no logic change)
- `refactor:` Code refactoring
- `test:` Test additions/updates
- `chore:` Maintenance tasks
- `perf:` Performance improvements

Examples:
```
feat: add bulk email notification system

Add ability to send emails to multiple recipients in batches
with progress tracking and error handling.

Fixes #123
```

```
fix: resolve picture upload deadline calculation

The picture_upload_deadline method was returning incorrect
time by not accounting for timezone differences.

Fixes #456
```

## Testing

### Running Tests

```bash
python manage.py test
```

### Writing Tests

- Write unit tests for new functions
- Write integration tests for features
- Achieve reasonable coverage
- Test both success and failure cases

Example:
```python
from django.test import TestCase
from accounts.models import CustomUser, Department

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Programming")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_picture_upload_deadline(self):
        """Test that picture upload deadline is 72 hours"""
        deadline = self.user.picture_upload_deadline()
        self.assertIsNotNone(deadline)
```

## Documentation

### Update Documentation When:

- Adding new features
- Changing existing behavior
- Adding environment variables
- Modifying deployment process
- Updating security practices

### Documentation Files:

- `README.md` - Project overview
- `CONTRIBUTING.md` - This file
- `CODE_OF_CONDUCT.md` - Community standards
- `CHANGELOG.md` - Version history
- `DOCKER_GUIDE.md` - Docker setup
- Code comments - Inline documentation

## Team & Contributors

This project is maintained by the ICT Club Development Team at Mwenge Catholic University.

### Current Contributors

#### Lead Developer
- Clever Godson (@cleven12) - Project architect, core features, Docker setup

#### Contributors
- Community members (contributions welcome)

### How to Be Listed

To be listed as a contributor:

1. Make meaningful contributions to the project
2. Follow the Code of Conduct
3. Your pull requests will be reviewed and merged
4. You'll be added to the contributors list after your first merged PR

### Task Areas

Feel free to contribute in these areas:

**Frontend Development**
- UI/UX improvements
- Template refactoring
- JavaScript enhancements
- Mobile responsiveness

**Backend Development**
- API development (future)
- Database optimization
- Email system improvements
- Security enhancements

**DevOps & Infrastructure**
- Docker improvements
- Deployment automation
- Configuration management
- CI/CD pipeline

**Documentation**
- README improvements
- Setup guides
- Troubleshooting guides
- Code documentation

**Testing**
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests

**Bug Fixes**
- Issue resolution
- Performance optimization
- Security patches
- Error handling

## Review Process

1. Submit pull request
2. Automated tests run
3. Code review by maintainers
4. Address feedback
5. Final approval
6. Merge to main branch

## Deployment

Only maintainers can deploy to production. After your PR is merged:

- Code goes into the main branch
- Tests run automatically
- Deployment happens on schedule
- Version is updated in CHANGELOG.md

## Questions?

- Check existing issues and discussions
- Review documentation
- Ask in pull request comments
- Contact maintainers

## Thank You

Thank you for contributing to the MWECAU ICT Club Platform! Your efforts help make this project better for everyone.

---

**Last Updated:** December 13, 2025  
**Maintained By:** ICT Club Development Team
