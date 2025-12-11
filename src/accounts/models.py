from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator


class Department(models.Model):
    """Department in ICT Club"""
    DEPARTMENT_CHOICES = [
        ('programming', 'Programming'),
        ('cybersecurity', 'Cybersecurity'),
        ('networking', 'Networking'),
        ('maintenance', 'Computer Maintenance'),
        ('design', 'Graphic Design'),
        ('ai_ml', 'AI & Machine Learning'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    leader = models.OneToOneField(
        'CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_department'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """Courses available in the system"""
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """Custom user model with club-specific fields"""
    reg_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Registration Number',
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\-/]+$',
                message='Registration number contains invalid characters'
            )
        ]
    )
    full_name = models.CharField(max_length=200)
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='members'
    )
    course_other = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Other Course (if not listed)',
        help_text='Specify your course if not in the dropdown'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='members'
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Account Approved by Admin/Leader'
    )
    picture = models.ImageField(
        upload_to='profile_pictures/%Y/%m/',
        null=True,
        blank=True,
        verbose_name='Profile Picture'
    )
    picture_uploaded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Picture Upload Time'
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Role indicators
    is_department_leader = models.BooleanField(
        default=False,
        verbose_name='Is Department Leader'
    )
    is_katibu = models.BooleanField(
        default=False,
        verbose_name='Is Katibu (Secretary)'
    )
    is_katibu_assistance = models.BooleanField(
        default=False,
        verbose_name='Is Katibu Assistance'
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-registered_at']
        indexes = [
            models.Index(fields=['reg_number']),
            models.Index(fields=['is_approved', 'registered_at']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.reg_number})"
    
    def is_leadership(self):
        """Check if user is in leadership (Admin, Katibu, or Department Leader)"""
        return self.is_staff or self.is_katibu or self.is_katibu_assistance or self.is_department_leader
    
    def picture_upload_deadline(self):
        """Returns the deadline for picture upload (72 hours after registration)"""
        if self.registered_at:
            return self.registered_at + timezone.timedelta(hours=72)
        return None
    
    def is_picture_overdue(self):
        """Check if picture upload deadline has passed"""
        if not self.picture and self.registered_at:
            return timezone.now() > self.picture_upload_deadline()
        return False
    
    def time_until_picture_deadline(self):
        """Returns timedelta until picture deadline"""
        deadline = self.picture_upload_deadline()
        if deadline:
            return deadline - timezone.now()
        return None
