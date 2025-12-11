"""
Constants and configuration for ICT Club
"""

# Department Slugs
DEPARTMENTS = {
    'programming': 'Programming',
    'cybersecurity': 'Cybersecurity',
    'networking': 'Networking',
    'maintenance': 'Computer Maintenance',
    'design': 'Graphic Design',
    'ai_ml': 'AI & Machine Learning',
}

# Membership Fee (in TZS)
MEMBERSHIP_FEE = 15000

# Picture Upload Deadline (hours)
PICTURE_UPLOAD_DEADLINE = 72

# Approved Member Permissions
MEMBER_PERMISSIONS = [
    'can_view_dashboard',
    'can_update_profile',
    'can_upload_picture',
    'can_access_projects',
    'can_view_announcements',
]

# Department Leader Permissions
LEADER_PERMISSIONS = [
    'can_approve_members',
    'can_reject_members',
    'can_view_department_members',
    'can_update_department',
]

# Admin Permissions
ADMIN_PERMISSIONS = [
    'can_manage_all_members',
    'can_manage_departments',
    'can_manage_courses',
    'can_view_payment_records',
    'can_access_admin_panel',
]

# Email Templates
EMAIL_TEMPLATES = {
    'registration': 'emails/registration_confirmation.html',
    'approval': 'emails/member_approved.html',
    'rejection': 'emails/member_rejected.html',
    'picture_reminder': 'emails/picture_reminder.html',
    'announcement': 'emails/announcement.html',
}

# Messages
MESSAGES = {
    'registration_success': 'Registration successful! Your account is pending approval.',
    'approval_success': 'Member account has been approved.',
    'rejection_success': 'Member account has been rejected.',
    'picture_upload_success': 'Profile picture uploaded successfully.',
    'profile_update_success': 'Profile updated successfully!',
}
