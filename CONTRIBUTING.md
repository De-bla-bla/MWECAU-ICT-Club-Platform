# Contributing Guide

Thank you for your interest in contributing to the MWECAU ICT Club website! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Respect different perspectives
- Report violations to maintainers

## Getting Started

### 1. Fork the Repository

```bash
git clone https://github.com/yourusername/mwecau_ict.git
cd mwecau_ict
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Tests

### 3. Make Changes

Make your changes following the coding standards below.

### 4. Test Your Changes

```bash
python src/manage.py test
```

### 5. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git commit -m "feat: add new feature description"
git commit -m "fix: resolve issue with component"
git commit -m "docs: update API documentation"
git commit -m "test: add tests for feature"
git commit -m "refactor: improve code structure"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Coding Standards

### Python Style Guide (PEP 8)

```python
# Good
def calculate_total(items: list) -> float:
    """Calculate total from items."""
    return sum(item.price for item in items)

# Bad
def calculateTotal(items):
    return sum(i.price for i in items)
```

### Django Best Practices

1. **Models**
   - Use descriptive names
   - Add docstrings
   - Include default values
   - Create indexes for frequently queried fields

2. **Views**
   - Use class-based views
   - Add proper permission checks
   - Include error handling
   - Document with docstrings

3. **Forms**
   - Validate user input
   - Add help text
   - Use appropriate widgets
   - Test edge cases

4. **Serializers**
   - Document all fields
   - Include validation
   - Handle nested relationships
   - Test serialization

### Template Standards

```html
<!-- Good -->
<div class="card">
    <div class="card-header">
        <h5 class="card-title">{{ title }}</h5>
    </div>
    <div class="card-body">
        {% for item in items %}
            <p>{{ item }}</p>
        {% endfor %}
    </div>
</div>

<!-- Bad -->
<div>
    <h5>{{ title }}</h5>
    <p>
        {% for i in items %}
            {{ i }}
        {% endfor %}
    </p>
</div>
```

## Testing Guidelines

### Unit Tests

```python
from django.test import TestCase

class ModelTest(TestCase):
    """Test cases for model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.object = Model.objects.create(name='Test')
    
    def test_creation(self):
        """Test object creation."""
        self.assertEqual(self.object.name, 'Test')
    
    def test_str_representation(self):
        """Test string representation."""
        self.assertEqual(str(self.object), 'Test')
```

### Run Tests

```bash
# All tests
python src/manage.py test

# Specific app
python src/manage.py test accounts

# Specific test
python src/manage.py test accounts.tests.ModelTest.test_creation

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## Documentation

### Docstring Format

```python
def function_name(param1, param2):
    """
    Brief description of function.
    
    Longer description if needed, explaining the behavior
    and any important details.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
    
    Returns:
        bool: Description of return value
    
    Raises:
        ValueError: When value is invalid
    
    Example:
        >>> result = function_name('test', 5)
        >>> result
        True
    """
    pass
```

### Comment Guidelines

```python
# Good - explains WHY
if user.is_picture_overdue():
    # Picture deadline was 72 hours ago, enforce upload
    return redirect('upload_picture')

# Bad - explains WHAT (which is obvious)
# Check if picture is overdue
if user.is_picture_overdue():
    return redirect('upload_picture')
```

## Pull Request Process

### Before Submitting

1. Update tests
2. Update documentation
3. Add changelog entry
4. Run full test suite
5. Check code style

### PR Description Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added tests
- [ ] All tests pass
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

## Issues and Bug Reports

### Reporting a Bug

```markdown
## Description
Clear description of the bug.

## Steps to Reproduce
1. First step
2. Second step
3. Expected behavior
4. Actual behavior

## Environment
- OS: 
- Python version:
- Django version:

## Additional Context
Screenshots, logs, etc.
```

### Feature Requests

```markdown
## Description
Description of desired feature.

## Use Case
Why this feature is needed.

## Proposed Solution
How to implement it.

## Alternative Solutions
Other ways to solve this.
```

## Project Structure

```
mwecau_ict/
├── src/
│   ├── config/              # Project settings
│   ├── accounts/            # User management
│   ├── core/               # Core functionality
│   ├── membership/         # Membership management
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JS, images
│   ├── manage.py
│   └── db.sqlite3
├── tests/                  # Test suite
├── docs/                   # Documentation
├── .env.example           # Example environment
├── requirements.txt       # Dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker compose
└── README.md            # Project readme
```

## Useful Commands

```bash
# Create migrations
python src/manage.py makemigrations

# Run migrations
python src/manage.py migrate

# Create superuser
python src/manage.py createsuperuser

# Run development server
python src/manage.py runserver

# Django shell
python src/manage.py shell

# Run tests with coverage
coverage run --source='.' src/manage.py test
coverage report
coverage html

# Format code
black src/

# Check linting
flake8 src/

# Security check
python -m safety check
```

## Review Process

1. Automated checks (tests, linting)
2. Code review by maintainers
3. Feedback and changes requested if needed
4. Approval and merge

## Questions?

- Check existing issues and discussions
- Ask in the pull request
- Contact maintainers
- Check documentation

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- GitHub commit history
- Release notes

Thank you for contributing!
