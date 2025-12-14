"""
Email System Testing Guide
Comprehensive testing procedures for email functionality
"""

# ============================================================================
# TEST 1: VERIFY EMAIL CONFIGURATION
# ============================================================================

def test_email_configuration():
    """Verify all email settings are correctly configured"""
    from django.conf import settings
    from accounts.email_service import EmailService
    
    print("\n" + "="*60)
    print("TEST 1: Email Configuration Validation")
    print("="*60)
    
    # Check required settings
    required_settings = [
        ('EMAIL_HOST', settings.EMAIL_HOST),
        ('EMAIL_PORT', settings.EMAIL_PORT),
        ('EMAIL_USE_TLS', settings.EMAIL_USE_TLS),
        ('EMAIL_HOST_USER', settings.EMAIL_HOST_USER),
        ('DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL),
    ]
    
    all_valid = True
    for setting_name, setting_value in required_settings:
        status = "✓" if setting_value else "✗"
        print(f"{status} {setting_name}: {setting_value}")
        if not setting_value:
            all_valid = False
    
    # Validate configuration
    if EmailService._validate_email_config():
        print("\n✓ Email configuration is VALID")
    else:
        print("\n✗ Email configuration is INVALID")
        return False
    
    return True


# ============================================================================
# TEST 2: SEND TEST EMAIL
# ============================================================================

def test_send_single_email():
    """Test sending a single email"""
    from accounts.email_service import EmailService
    
    print("\n" + "="*60)
    print("TEST 2: Send Single Email")
    print("="*60)
    
    test_email = "test@example.com"
    
    print(f"Sending test email to: {test_email}")
    
    success, error = EmailService.send_single_email(
        subject="Test Email - ICT Club",
        recipient_email=test_email,
        html_template="emails/test_email.html",
        context={'recipient_email': test_email},
        plain_message="Test email from ICT Club",
        fail_silently=False
    )
    
    if success:
        print("✓ Email sent successfully!")
        return True
    else:
        print(f"✗ Email failed: {error}")
        return False


# ============================================================================
# TEST 3: SEND APPROVAL EMAIL
# ============================================================================

def test_send_approval_email():
    """Test sending approval email to a user"""
    from accounts.models import CustomUser
    from accounts.email_service import EmailService
    
    print("\n" + "="*60)
    print("TEST 3: Send Approval Email")
    print("="*60)
    
    try:
        # Get first user
        user = CustomUser.objects.first()
        if not user:
            print("✗ No users found in database")
            return False
        
        print(f"Sending approval email to: {user.full_name} ({user.email})")
        
        success, error = EmailService.send_approval_email(user)
        
        if success:
            print("✓ Approval email sent successfully!")
            return True
        else:
            print(f"✗ Approval email failed: {error}")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False


# ============================================================================
# TEST 4: SEND REGISTRATION EMAIL
# ============================================================================

def test_send_registration_email():
    """Test sending registration confirmation email"""
    from accounts.models import CustomUser, Department
    from accounts.email_service import EmailService
    
    print("\n" + "="*60)
    print("TEST 4: Send Registration Email")
    print("="*60)
    
    try:
        user = CustomUser.objects.first()
        if not user:
            print("✗ No users found in database")
            return False
        
        print(f"Sending registration email to: {user.email}")
        
        success, error = EmailService.send_registration_email(user, user.department)
        
        if success:
            print("✓ Registration email sent successfully!")
            return True
        else:
            print(f"✗ Registration email failed: {error}")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False


# ============================================================================
# TEST 5: SEND BULK EMAILS
# ============================================================================

def test_send_bulk_emails():
    """Test sending emails to multiple recipients"""
    from accounts.models import CustomUser
    from accounts.email_service import EmailService
    
    print("\n" + "="*60)
    print("TEST 5: Send Bulk Emails")
    print("="*60)
    
    try:
        # Get first 5 users
        recipients = list(
            CustomUser.objects.all()[:5].values_list('email', flat=True)
        )
        
        if not recipients:
            print("✗ No users found in database")
            return False
        
        print(f"Sending bulk email to {len(recipients)} recipients")
        
        results = EmailService.send_bulk_emails(
            subject="Test Bulk Email",
            recipients=recipients,
            html_template="emails/announcement.html",
            context_data={'title': 'Test Announcement'},
            fail_silently=True
        )
        
        print(f"Total: {results['total']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
        
        if results['successful'] > 0:
            print("✓ Bulk email sent successfully!")
            return True
        else:
            print("✗ No emails were sent successfully")
            if results['errors']:
                print("Errors:", results['errors'][:3])
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False


# ============================================================================
# TEST 6: SEND REJECTION EMAIL
# ============================================================================

def test_send_rejection_email():
    """Test sending rejection email"""
    from accounts.models import CustomUser
    from accounts.email_service import EmailService
    
    print("\n" + "="*60)
    print("TEST 6: Send Rejection Email")
    print("="*60)
    
    try:
        user = CustomUser.objects.filter(is_active=False).first()
        if not user:
            # Create a temporary test user
            user = CustomUser.objects.first()
        
        if not user:
            print("✗ No users found in database")
            return False
        
        print(f"Sending rejection email to: {user.email}")
        
        success, error = EmailService.send_rejection_email(user)
        
        if success:
            print("✓ Rejection email sent successfully!")
            return True
        else:
            print(f"✗ Rejection email failed: {error}")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False


# ============================================================================
# TEST 7: PICTURE REMINDER EMAIL
# ============================================================================

def test_send_picture_reminder_email():
    """Test sending picture reminder email"""
    from accounts.models import CustomUser
    from accounts.email_service import EmailService
    
    print("\n" + "="*60)
    print("TEST 7: Send Picture Reminder Email")
    print("="*60)
    
    try:
        user = CustomUser.objects.first()
        if not user:
            print("✗ No users found in database")
            return False
        
        print(f"Sending picture reminder to: {user.email}")
        
        success, error = EmailService.send_picture_reminder_email(user)
        
        if success:
            print("✓ Picture reminder email sent successfully!")
            return True
        else:
            print(f"✗ Picture reminder email failed: {error}")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False


# ============================================================================
# TEST 8: CONTACT MESSAGE NOTIFICATION
# ============================================================================

def test_send_contact_notification():
    """Test sending contact form notification"""
    from core.models import ContactMessage
    from accounts.email_service import EmailService
    
    print("\n" + "="*60)
    print("TEST 8: Send Contact Message Notification")
    print("="*60)
    
    try:
        # Get first contact message
        message = ContactMessage.objects.first()
        if not message:
            print("✗ No contact messages found in database")
            return False
        
        print(f"Sending notification for message from: {message.email}")
        
        success, error = EmailService.send_contact_message_notification(message)
        
        if success:
            print("✓ Contact notification sent successfully!")
            return True
        else:
            print(f"✗ Contact notification failed: {error}")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run all email tests and report results"""
    print("\n" + "="*60)
    print("EMAIL SYSTEM COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    tests = [
        ("Email Configuration", test_email_configuration),
        ("Send Single Email", test_send_single_email),
        ("Send Approval Email", test_send_approval_email),
        ("Send Registration Email", test_send_registration_email),
        ("Send Bulk Emails", test_send_bulk_emails),
        ("Send Rejection Email", test_send_rejection_email),
        ("Send Picture Reminder", test_send_picture_reminder_email),
        ("Send Contact Notification", test_send_contact_notification),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} - Exception: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED - Email system is working correctly!")
    else:
        print(f"\n✗ {total - passed} tests failed - Check configuration and logs")
    
    return passed == total


# ============================================================================
# DJANGO SHELL USAGE
# ============================================================================

# To use this in Django shell:
# python manage.py shell
# 
# Then run:
# from tests_email import run_all_tests
# run_all_tests()
#
# Or run individual tests:
# from tests_email import test_email_configuration
# test_email_configuration()
