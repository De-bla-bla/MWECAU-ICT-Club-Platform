"""
Form helper utilities and mixins
"""
from django import forms


class FormHelper:
    """Helper methods for form processing"""
    
    @staticmethod
    def add_bootstrap_classes(form, exclude_fields=None):
        """Add Bootstrap form-control classes to all form fields"""
        exclude_fields = exclude_fields or []
        
        for field_name, field in form.fields.items():
            if field_name in exclude_fields:
                continue
            
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-check-input'
                })
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({
                    'class': 'form-check-input'
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'rows': '4'
                })
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'accept': 'image/*'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control'
                })
    
    @staticmethod
    def set_field_placeholder(form, field_name, placeholder):
        """Set placeholder for a specific field"""
        if field_name in form.fields:
            form.fields[field_name].widget.attrs['placeholder'] = placeholder
    
    @staticmethod
    def set_field_help_text(form, field_name, help_text):
        """Set help text for a specific field"""
        if field_name in form.fields:
            form.fields[field_name].help_text = help_text
    
    @staticmethod
    def disable_field(form, field_name):
        """Disable a form field"""
        if field_name in form.fields:
            form.fields[field_name].disabled = True
    
    @staticmethod
    def make_field_required(form, field_name, required=True):
        """Set field as required or optional"""
        if field_name in form.fields:
            form.fields[field_name].required = required


class FormMixin:
    """Mixin to add Bootstrap styling to Django forms"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormHelper.add_bootstrap_classes(self)
    
    def add_error_message(self, field, message):
        """Add error message to a field"""
        self.add_error(field, message)


class BootstrapForm(forms.Form, FormMixin):
    """Base form class with Bootstrap styling included"""
    pass


class BootstrapModelForm(forms.ModelForm, FormMixin):
    """Base model form class with Bootstrap styling included"""
    pass


class DateInputWidget(forms.DateInput):
    """Custom date input widget with Bootstrap styling"""
    input_type = 'date'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'class': 'form-control',
        })


class TimeInputWidget(forms.TimeInput):
    """Custom time input widget with Bootstrap styling"""
    input_type = 'time'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'class': 'form-control',
        })


class EmailInputWidget(forms.EmailInput):
    """Custom email input widget with Bootstrap styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'class': 'form-control',
            'type': 'email',
        })


class PhoneInputWidget(forms.TextInput):
    """Custom phone input widget with Bootstrap styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'class': 'form-control',
            'type': 'tel',
            'pattern': '[0-9+\-\s()]*',
        })


class URLInputWidget(forms.URLInput):
    """Custom URL input widget with Bootstrap styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'class': 'form-control',
        })


class ColorPickerWidget(forms.TextInput):
    """Custom color picker widget"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'type': 'color',
            'class': 'form-control form-control-color',
        })
