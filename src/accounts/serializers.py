"""
Django REST Framework serializers for API endpoints
"""
from rest_framework import serializers
from accounts.models import CustomUser, Department, Course
from core.models import Project, Event, Announcement, ContactMessage
from membership.models import MembershipPayment


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'slug', 'description', 'color', 'member_count']
        read_only_fields = ['id', 'slug']
    
    def get_member_count(self, obj):
        return obj.custuser_set.count()


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model"""
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'department', 'member_count']
        read_only_fields = ['id']
    
    def get_member_count(self, obj):
        return obj.custuser_set.count()


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'reg_number', 'email', 'full_name', 'phone', 
            'department', 'department_name', 'course', 'course_name',
            'is_approved', 'picture', 'registered_at', 'is_department_leader',
            'is_katibu', 'is_katibu_assistance', 'role'
        ]
        read_only_fields = ['id', 'registered_at']
    
    def get_role(self, obj):
        from accounts.permissions import get_user_role
        return get_user_role(obj)


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'slug', 'image', 'github_url',
            'live_url', 'department', 'department_name', 'featured',
            'created_by', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_date', 'location',
            'department', 'department_name', 'image', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    """Serializer for Announcement model"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    type_display = serializers.CharField(source='get_announcement_type_display', read_only=True)
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'announcement_type', 'type_display',
            'department', 'department_name', 'is_published', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'subject', 'message',
            'is_responded', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MembershipPaymentSerializer(serializers.ModelSerializer):
    """Serializer for MembershipPayment model"""
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = MembershipPayment
        fields = [
            'id', 'user', 'user_name', 'amount', 'provider', 'status',
            'status_display', 'transaction_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserDetailSerializer(CustomUserSerializer):
    """Extended serializer for detailed user information"""
    department = DepartmentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    recent_activities = serializers.SerializerMethodField()
    
    def get_recent_activities(self, obj):
        from core.activity_log import ActivityLog
        activities = ActivityLog.objects.filter(user=obj).order_by('-created_at')[:5]
        return [{
            'action': a.action,
            'description': a.description,
            'created_at': a.created_at
        } for a in activities]


class ProjectDetailSerializer(ProjectSerializer):
    """Extended serializer for detailed project information"""
    department = DepartmentSerializer(read_only=True)
    created_by = CustomUserSerializer(read_only=True)
