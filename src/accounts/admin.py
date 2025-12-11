from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import CustomUser, Department, Course
from .forms import CustomUserCreationForm, CustomUserChangeForm


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'leader', 'member_count')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'member_count')
    search_fields = ('name', 'code')
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('full_name', 'email', 'reg_number', 'picture', 'picture_uploaded_at')
        }),
        ('Academic Information', {
            'fields': ('course', 'course_other', 'department')
        }),
        ('Club Status', {
            'fields': ('is_approved', 'approved_at', 'registered_at')
        }),
        ('Roles', {
            'fields': ('is_department_leader', 'is_katibu', 'is_katibu_assistance')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'reg_number'),
        }),
        ('Academic Information', {
            'classes': ('wide',),
            'fields': ('course', 'course_other', 'department'),
        }),
    )
    
    list_display = (
        'reg_number', 'full_name', 'email', 'department', 
        'is_approved_badge', 'picture_badge', 'is_department_leader',
        'registered_at'
    )
    list_filter = (
        'is_approved', 'is_active', 'is_department_leader', 
        'is_katibu', 'is_katibu_assistance', 'department', 'registered_at'
    )
    search_fields = ('full_name', 'email', 'reg_number', 'username')
    ordering = ('-registered_at',)
    readonly_fields = ('registered_at', 'approved_at', 'picture_uploaded_at', 'date_joined', 'last_login')
    
    actions = ['approve_members', 'reject_members', 'send_picture_reminder']
    
    def is_approved_badge(self, obj):
        """Display approval status as a colored badge"""
        if obj.is_approved:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Approved</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 3px 8px; border-radius: 3px;">⏳ Pending</span>'
            )
    is_approved_badge.short_description = 'Status'
    
    def picture_badge(self, obj):
        """Display picture upload status"""
        if obj.picture:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Uploaded</span>'
            )
        elif obj.is_picture_overdue():
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px;">✗ Overdue</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 3px;">⏳ Pending</span>'
            )
    picture_badge.short_description = 'Picture'
    
    def approve_members(self, request, queryset):
        """Bulk approve members"""
        updated = queryset.update(is_approved=True, approved_at=timezone.now())
        self.message_user(request, f'{updated} members have been approved.')
    approve_members.short_description = 'Approve selected members'
    
    def reject_members(self, request, queryset):
        """Bulk reject members"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} members have been rejected.')
    reject_members.short_description = 'Reject selected members'
    
    def send_picture_reminder(self, request, queryset):
        """Send picture upload reminder to members without picture"""
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        
        members_without_picture = queryset.filter(picture__isnull=True, picture='')
        count = 0
        for member in members_without_picture:
            if not member.is_picture_overdue():
                continue
            
            context = {'member': member}
            email_html = render_to_string('emails/picture_reminder.html', context)
            try:
                send_mail(
                    subject='Picture Upload Reminder - ICT Club',
                    message='Please upload your profile picture.',
                    from_email='mwecauictclub@gmail.com',
                    recipient_list=[member.email],
                    html_message=email_html,
                    fail_silently=False,
                )
                count += 1
            except Exception:
                pass
        
        self.message_user(request, f'Picture reminder sent to {count} members.')
    send_picture_reminder.short_description = 'Send picture upload reminder'


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

# Customize admin site
admin.site.site_header = 'ICT Club Administration'
admin.site.site_title = 'ICT Club Admin'
admin.site.index_title = 'Welcome to ICT Club Administration'

