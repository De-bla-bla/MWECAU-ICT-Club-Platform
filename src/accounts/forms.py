from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Course, Department
from .validators import validate_registration_number, validate_full_name, validate_strong_password


class CustomUserCreationForm(UserCreationForm):
    """Form for user registration with proper validation"""
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        empty_label="Select your course (optional)..."
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        empty_label="Select your department..."
    )
    email = forms.EmailField(
        required=True,
        help_text='Your university email address'
    )
    full_name = forms.CharField(
        max_length=200,
        required=True,
        help_text='Format: FirstName LastName Surname (e.g., John Doe Smith)',
        validators=[validate_full_name]
    )
    
    class Meta:
        model = CustomUser
        fields = ('reg_number', 'full_name', 'email', 'course', 'department', 'password1', 'password2')
        widgets = {
            'reg_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'T/DEG/2025/001',
                'pattern': r'^T/(DEG|CERT|DIP|MASTER|PHD)/\d{4}/\d{3,4}$'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'John Doe Smith'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@mwecau.ac.tz'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Strong password required',
            'id': 'password-input'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
        self.fields['course'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['department'].widget.attrs.update({
            'class': 'form-select'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email.lower()
    
    def clean_reg_number(self):
        reg_number = self.cleaned_data.get('reg_number').upper()
        if CustomUser.objects.filter(reg_number__iexact=reg_number).exists():
            raise ValidationError("This registration number is already in use.")
        validate_registration_number(reg_number)
        return reg_number
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_strong_password(password1)
        return password1
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        return full_name.strip()
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def save(self, commit=True):
        """Override save to use registration number as username"""
        user = super().save(commit=False)
        
        # Use registration number as username
        reg_number = self.cleaned_data.get('reg_number')
        user.username = reg_number.upper()
        
        # Ensure department is set from cleaned data
        if not user.department and 'department' in self.cleaned_data:
            user.department = self.cleaned_data['department']
        
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """Form for updating user profile"""
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        empty_label="Select your course..."
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        empty_label="Select your department..."
    )
    
    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'course', 'course_other', 'department', 'picture')
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'course': forms.Select(attrs={
                'class': 'form-select'
            }),
            'course_other': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify your course if not listed'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }


class PictureUploadForm(forms.ModelForm):
    """Form for uploading profile picture"""
    class Meta:
        model = CustomUser
        fields = ('picture',)
        widgets = {
            'picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
