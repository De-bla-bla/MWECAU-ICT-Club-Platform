from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Course, Department


class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
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
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )
    
    class Meta:
        model = CustomUser
        fields = ('reg_number', 'full_name', 'email', 'course', 'course_other', 'department', 'password1', 'password2')
        widgets = {
            'reg_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E.g., MWE/CS/2022/001'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@mwecau.ac.tz'
            }),
            'course_other': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify your course'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
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
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email
    
    def clean_reg_number(self):
        reg_number = self.cleaned_data.get('reg_number').upper()
        if CustomUser.objects.filter(reg_number__iexact=reg_number).exists():
            raise ValidationError("This registration number is already in use.")
        return reg_number
    
    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        course_other = cleaned_data.get('course_other')
        
        # If course is not selected, course_other must be provided
        if not course and not course_other:
            raise ValidationError("Please select a course or specify your course in the 'Other' field.")
        
        return cleaned_data


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
