from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Event, Announcement, ContactMessage


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'featured_badge', 'created_by', 'created_at')
    list_filter = ('featured', 'department', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'image')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url')
        }),
        ('Organization', {
            'fields': ('department', 'created_by', 'featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def featured_badge(self, obj):
        if obj.featured:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 3px 8px; border-radius: 3px;">⭐ Featured</span>'
            )
        return '—'
    featured_badge.short_description = 'Status'


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'department', 'location', 'created_at')
    list_filter = ('department', 'event_date', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Details', {
            'fields': ('event_date', 'location', 'department')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'announcement_type', 'department', 'created_by',
        'published_badge', 'created_at'
    )
    list_filter = ('announcement_type', 'published', 'department', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Announcement', {
            'fields': ('title', 'content', 'announcement_type')
        }),
        ('Organization', {
            'fields': ('department', 'created_by', 'published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def published_badge(self, obj):
        if obj.published:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Published</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px;">Draft</span>'
            )
    published_badge.short_description = 'Status'


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'responded_badge', 'created_at')
    list_filter = ('responded', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    
    actions = ['mark_as_responded']
    
    def responded_badge(self, obj):
        if obj.responded:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Responded</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 3px 8px; border-radius: 3px;">⏳ Pending</span>'
            )
    responded_badge.short_description = 'Status'
    
    def mark_as_responded(self, request, queryset):
        count = queryset.update(responded=True)
        self.message_user(request, f'{count} messages marked as responded.')
    mark_as_responded.short_description = 'Mark as responded'


admin.site.register(Project, ProjectAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
