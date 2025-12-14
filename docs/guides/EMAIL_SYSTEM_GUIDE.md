# Email System Documentation

## Overview

The ICT Club platform includes a robust email system with comprehensive error handling, logging, and support for bulk email operations. All email functionality is centralized in the `EmailService` class for consistency and maintainability.

## Email Service Class

### Location
`src/accounts/email_service.py`

### Features
- **Error Handling**: All methods have try-catch blocks with detailed logging
- **Bulk Email Support**: Send emails to multiple recipients with batch processing
- **Template Support**: Renders HTML templates for professional emails
- **Logging**: All operations are logged for debugging and monitoring
- **Configuration Validation**: Automatically validates email settings before sending
- **Backward Compatibility**: Legacy standalone functions still work

## Configuration

Email configuration is set in `src/config/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='mwecauictclub@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='mwecauictclub@gmail.com')
```

Set these environment variables in your `.env` file:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## Usage Examples

### 1. Send Registration Email

```python
from accounts.email_service import EmailService

user = User.objects.get(id=1)
success, error = EmailService.send_registration_email(user, user.department)

if success:
    print("Email sent successfully")
else:
    print(f"Error: {error}")
```

### 2. Send Approval Email

```python
success, error = EmailService.send_approval_email(user)
if not success:
    logger.error(f"Failed to send approval: {error}")
```

### 3. Send Bulk Announcement Email

```python
recipients = CustomUser.objects.filter(is_approved=True).values_list('email', flat=True)
results = EmailService.send_bulk_emails(
    subject='Important Announcement',
    recipients=list(recipients),
    html_template='emails/announcement.html',
    context_data={'title': 'Announcement Title', 'content': 'Content here'},
    fail_silently=True,
    batch_size=100
)

print(f"Successful: {results['successful']}, Failed: {results['failed']}")
```

### 4. Send Single Email with Custom Template

```python
success, error = EmailService.send_single_email(
    subject='Custom Email',
    recipient_email='user@example.com',
    html_template='emails/custom_template.html',
    context={'user': user, 'data': some_data},
    plain_message='Fallback text message',
    fail_silently=False
)
```

## Management Commands

### Send Bulk Email Command

**Usage:**
```bash
# Send to all approved members
python manage.py send_bulk_email --type=announcement --target=approved_members \
  --subject="Important Update" --template=emails/announcement.html

# Send to specific department
python manage.py send_bulk_email --type=announcement --target=department \
  --department=Programming --subject="Department Announcement"

# Send to specific email addresses
python manage.py send_bulk_email --type=manual \
  --recipients=user1@example.com,user2@example.com \
  --subject="Manual Email"

# Send to all active members
python manage.py send_bulk_email --type=announcement --target=all_members \
  --subject="Club Update"

# Send to pending members
python manage.py send_bulk_email --type=announcement --target=pending_members \
  --subject="Your Application Status"
```

**Options:**
- `--type`: `announcement` or `manual` (required)
- `--target`: `all_members`, `approved_members`, `pending_members`, or `department`
- `--department`: Department name/slug (required if target=department)
- `--recipients`: Comma-separated emails (required if type=manual)
- `--subject`: Email subject (required)
- `--template`: Path to HTML template (default: emails/announcement.html)
- `--message`: Plain text message (optional)

### Test Email Command

**Usage:**
```bash
# Check email configuration
python manage.py test_email --check-config

# Send test email to specific address
python manage.py test_email --recipient=user@example.com

# Send test email to user by ID
python manage.py test_email --test-user=1
```

**Output Example:**
```
Email Configuration:
  EMAIL_BACKEND: django.core.mail.backends.smtp.EmailBackend
  EMAIL_HOST: smtp.gmail.com
  EMAIL_PORT: 587
  EMAIL_USE_TLS: True
  EMAIL_HOST_USER: mwecauictclub@gmail.com
  DEFAULT_FROM_EMAIL: mwecauictclub@gmail.com

✓ Email configuration is valid!
✓ Test email sent successfully to user@example.com
```

## Return Values

### Single Email Methods
Return a tuple: `(success: bool, error_message: Optional[str])`

```python
success, error = EmailService.send_approval_email(user)
if success:
    logger.info("Email sent")
else:
    logger.error(f"Failed: {error}")
```

### Bulk Email Methods
Return a dictionary:
```python
{
    'total': 100,           # Total recipients processed
    'successful': 98,       # Successfully sent
    'failed': 2,           # Failed sends
    'errors': [...]        # List of error messages
}
```

## Email Templates

All email templates are stored in `src/templates/emails/`:

- `registration_confirmation.html` - New user registration
- `member_approved.html` - Account approval
- `member_rejected.html` - Account rejection
- `picture_reminder.html` - Picture upload reminder
- `announcement.html` - General announcements
- `contact_message.html` - Contact form notifications
- `new_registration_admin.html` - Admin notification
- `new_registration_leader.html` - Department leader notification
- `test_email.html` - Test email template

## Error Handling

### Configuration Validation
```python
# Automatically checks:
- EMAIL_HOST is configured
- EMAIL_HOST_USER is configured
- EMAIL_HOST_PASSWORD is set (warns if not)
```

### Template Rendering Errors
```python
# Caught and logged:
- Invalid template paths
- Missing template variables
- Rendering exceptions
```

### SMTP Errors
```python
# Logged with full stack trace:
- Connection failures
- Authentication errors
- SMTP server errors
- Network timeouts
```

## Logging

All email operations are logged to Django's logging system. Configure in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/email.log',
        },
    },
    'loggers': {
        'accounts.email_service': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
        },
    },
}
```

## Backward Compatibility

Legacy functions still work for existing code:

```python
# Old way (still works)
from accounts.email_service import send_approval_email
send_approval_email(user)  # Returns bool

# New way (recommended)
from accounts.email_service import EmailService
success, error = EmailService.send_approval_email(user)
```

## Performance Considerations

### Batch Processing
Bulk emails are sent in configurable batches (default: 100 per batch) to avoid overwhelming the server.

### Fail-Silently Option
- `fail_silently=True`: Continues on errors, useful for non-critical emails
- `fail_silently=False`: Raises exceptions, useful for critical emails

### Timeout
Default SMTP timeout is set by Django (varies by backend). For slow connections, adjust in settings:
```python
EMAIL_TIMEOUT = 10  # seconds
```

## Testing

### Unit Tests
```python
from django.test import TestCase
from accounts.email_service import EmailService
from accounts.models import CustomUser

class EmailServiceTest(TestCase):
    def test_send_approval_email(self):
        user = CustomUser.objects.create_user(...)
        success, error = EmailService.send_approval_email(user)
        self.assertTrue(success)
        self.assertIsNone(error)
```

### Integration Tests
```bash
python manage.py test accounts.tests.EmailServiceTests
```

## Troubleshooting

### "Email configuration not properly configured"
- Check EMAIL_HOST is set
- Check EMAIL_HOST_USER is set
- Check EMAIL_HOST_PASSWORD is set

### "Failed to render email template"
- Verify template path is correct
- Ensure template exists in `templates/` directory
- Check template syntax and variables

### "Failed to send email to..."
- Check recipient email is valid
- Verify SMTP credentials are correct
- Check SMTP server is reachable
- Look in logs for detailed error messages

### Gmail-Specific Issues
If using Gmail:
1. Enable "Less secure apps" or create an app-specific password
2. Use app-specific password instead of Gmail password
3. Enable 2-factor authentication if needed

## Security Best Practices

1. **Never hardcode credentials** - Use environment variables
2. **Use fail_silently=True** for non-critical emails to prevent info leaks
3. **Sanitize user input** in email templates
4. **Log errors** but don't expose sensitive data in error messages
5. **Rate limit** bulk email operations to prevent abuse
6. **Monitor** email logs for suspicious activity

## Future Enhancements

Potential improvements:
- Email scheduling/queuing with Celery
- Email verification/bounce handling
- Unsubscribe functionality
- Email analytics tracking
- Template preview system
- Bulk email progress tracking
- Email retry mechanism for failed sends
