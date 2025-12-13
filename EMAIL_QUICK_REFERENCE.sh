#!/bin/bash
# Email System Quick Reference Guide
# Demonstrates all email functionality with examples

# ============================================================================
# TEST EMAIL CONFIGURATION
# ============================================================================

echo "=== Testing Email Configuration ==="
python manage.py test_email --check-config

echo ""
echo "=== Sending Test Email ==="
python manage.py test_email --recipient=user@example.com

echo ""
echo "=== Sending Test Email to User ==="
python manage.py test_email --test-user=1


# ============================================================================
# BULK EMAIL OPERATIONS
# ============================================================================

echo ""
echo "=== Send to All Active Members ==="
python manage.py send_bulk_email \
  --type=announcement \
  --target=all_members \
  --subject="Important Club Update" \
  --template=emails/announcement.html \
  --message="Check our new announcements!"

echo ""
echo "=== Send to Approved Members Only ==="
python manage.py send_bulk_email \
  --type=announcement \
  --target=approved_members \
  --subject="Member Exclusive Update"

echo ""
echo "=== Send to Pending Members ==="
python manage.py send_bulk_email \
  --type=announcement \
  --target=pending_members \
  --subject="Your Application Status"

echo ""
echo "=== Send to Specific Department ==="
python manage.py send_bulk_email \
  --type=announcement \
  --target=department \
  --department=Programming \
  --subject="Programming Department Update"

echo ""
echo "=== Send to Specific Email Addresses ==="
python manage.py send_bulk_email \
  --type=manual \
  --recipients=john@example.com,jane@example.com,admin@example.com \
  --subject="Custom Manual Email"


# ============================================================================
# PYTHON USAGE EXAMPLES
# ============================================================================

# Example 1: Send Single Email
# --------------------------
# from accounts.email_service import EmailService
# 
# success, error = EmailService.send_approval_email(user)
# if success:
#     print("Email sent!")
# else:
#     print(f"Error: {error}")

# Example 2: Send Bulk Emails
# ---------------------------
# from accounts.email_service import EmailService
# from accounts.models import CustomUser
# 
# recipients = CustomUser.objects.filter(
#     is_approved=True
# ).values_list('email', flat=True)
# 
# results = EmailService.send_bulk_emails(
#     subject="Important Announcement",
#     recipients=list(recipients),
#     html_template="emails/announcement.html",
#     context_data={'title': 'Annual Report'},
#     fail_silently=True
# )
# 
# print(f"Sent: {results['successful']}/{results['total']}")
# if results['failed'] > 0:
#     print(f"Failed: {results['failed']}")

# Example 3: Send Custom Email
# ----------------------------
# success, error = EmailService.send_single_email(
#     subject="Custom Message",
#     recipient_email="user@example.com",
#     html_template="emails/custom.html",
#     context={'user': user, 'data': some_data},
#     plain_message="Fallback text",
#     fail_silently=False
# )

# Example 4: Send Admin Notification
# ----------------------------------
# admin_emails = CustomUser.objects.filter(
#     is_staff=True
# ).values_list('email', flat=True)
# 
# results = EmailService.send_admin_notification(
#     admin_emails=list(admin_emails),
#     subject="New User Registration",
#     html_template="emails/new_registration_admin.html",
#     context={'user': new_user}
# )
