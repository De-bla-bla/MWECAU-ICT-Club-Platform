# Security Policy

## Reporting a Vulnerability

We take the security of the MWECAU ICT Club Platform very seriously. If you discover a security vulnerability, please report it responsibly to ensure we can address it promptly.

### How to Report

Please DO NOT create a public GitHub issue for security vulnerabilities. Instead:

1. **Email us directly** at: mwecauictclub@gmail.com(or contact repository maintainers)
2. **Include details:**
   - Type of vulnerability
   - Location in the codebase (file path, line number if possible)
   - Description of the vulnerability
   - Steps to reproduce (if applicable)
   - Potential impact
   - Suggested fix (if you have one)

3. **Allow 90 days** for us to address the issue before public disclosure

### What to Expect

- We will acknowledge receipt of your report within 48 hours
- We will provide regular updates on our progress
- We will credit you appropriately in the security advisory (unless you prefer anonymity)
- We will follow responsible disclosure practices

---

## Security Best Practices

### For Users

- Keep your password strong and unique
- Use a password manager to store credentials
- Enable two-factor authentication if available
- Never share your login credentials
- Report suspicious activity immediately
- Review your profile regularly for unauthorized changes

### For Developers

- Never commit secrets, API keys, or credentials to the repository
- Use environment variables for sensitive configuration
- Follow Django's security documentation
- Keep dependencies up-to-date
- Run security linters and scanners
- Conduct code reviews with security in mind
- Use HTTPS for all communications
- Validate and sanitize all user input

---

## Security Features Implemented

### Authentication Security

- Custom authentication backend supporting multiple credential types
- PBKDF2 password hashing (Django default)
- Password strength validation requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character
- Case-insensitive credential matching prevents user enumeration
- Session security with configurable timeout
- Rate limiting on login attempts
- Audit logging for authentication events

### Authorization & Access Control

- Role-based access control (RBAC)
- Django permission system integration
- Staff-only view protection
- Department leader authorization
- Custom decorators for permission checks
- Ownership-based authorization for profile edits
- Secure password reset flow

### Data Protection

- CSRF protection on all forms
- XSS prevention via Django template auto-escaping
- SQL injection prevention via Django ORM
- Email address validation
- Profile picture security scanning
- Secure file uploads with type validation
- Encrypted database in production

### Application Security

- Security headers configured:
  - Content-Security-Policy
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection
  - Strict-Transport-Security (HTTPS only)

- HTTPS enforcement in production
- Secure cookie settings:
  - HttpOnly flag
  - Secure flag (HTTPS only)
  - SameSite attribute
- CORS properly configured
- API rate limiting

### Database Security

- Unique constraints on sensitive fields:
  - Email addresses
  - Registration numbers
  - Usernames
- Foreign key relationships maintain data integrity
- Database encryption in production
- Regular backup procedures
- Access logs for admin operations
- Soft deletes for historical records (where applicable)

### Email Security

- Email addresses validated before sending
- Sensitive data not included in email subject lines
- Unsubscribe links in bulk communications
- Email verification during registration
- Secure sender authentication
- No credentials transmitted via email

### Deployment Security

- Environment variables for secrets management
- No hardcoded credentials in source code
- Docker container security scanning
- Dependency vulnerability scanning
- Regular security patches
- Web server (Nginx) security hardening
- Process isolation in containers
- Resource limits (memory, CPU)

---

## Dependency Management

### Regular Updates

We maintain dependencies with:
- Django security updates (critical patches within 24 hours)
- Python package security updates (within 1 week)
- Third-party library vulnerability scanning
- Automated dependency checking

### Known Vulnerabilities

Current status of known vulnerabilities:
- All identified vulnerabilities have been patched
- No unresolved high-severity issues
- Security monitoring enabled via GitHub Dependabot

---

## Secure Coding Standards

### Code Review Requirements

All code changes must:
1. Pass automated security linting
2. Have no hardcoded secrets
3. Include proper input validation
4. Have adequate error handling
5. Follow Django security documentation
6. Be reviewed by at least one maintainer

### Security Testing

- Unit tests for security-critical functions
- Integration tests for authentication flows
- Penetration testing in staging environment
- OWASP Top 10 vulnerability checks
- SQL injection testing
- XSS payload testing
- CSRF protection validation

---

## Incident Response Plan

In the event of a security breach:

1. **Containment** (immediate)
   - Disable affected accounts/features
   - Gather evidence
   - Alert team members

2. **Investigation** (within 24 hours)
   - Determine scope and impact
   - Identify root cause
   - Assess data exposure

3. **Notification** (within 48 hours)
   - Notify affected users
   - Provide guidance on next steps
   - Offer support and monitoring

4. **Resolution** (within 72 hours)
   - Patch vulnerability
   - Deploy fix to production
   - Verify remediation

5. **Post-Incident** (within 1 week)
   - Complete security audit
   - Implement preventive measures
   - Document lessons learned
   - Update security policies

---

## Compliance

This project maintains compliance with:

- OWASP Top 10 security standards
- Django security best practices
- General Data Protection Regulation (GDPR) principles
- Personal data protection guidelines
- University security policies
- Industry security standards

---

## Contact Information

For security-related inquiries:

- Security Team: security@mwecau.ac.tz
- Repository Maintainers: See [CONTRIBUTORS.md](CONTRIBUTORS.md)
- GitHub Issues: For non-security issues only

---

## Security Advisories

When a security vulnerability is fixed, we will:

1. Create a security advisory on GitHub
2. Release a patched version
3. Notify all users
4. Provide mitigation steps
5. Document the fix

Past security advisories can be found in the [GitHub Security Advisories](https://github.com/mwecauictclub/MWECAU-ICT-Club-Platform/security/advisories) section.

---

## Recognition

We appreciate responsible vulnerability reporting and will:

- Acknowledge security researchers in our security advisories
- Provide public credit (if desired)
- Consider contributors for security team membership
- Feature outstanding security contributions

Thank you for helping keep our community safe!

