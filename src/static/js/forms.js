"""
Frontend form utilities and JavaScript helper functions
"""
from django.forms import ModelForm, Form
from django.forms.widgets import DateInput, TimeInput, EmailInput


class FormValidationHelper:
    """Helper class for form validation on frontend"""
    
    @staticmethod
    def get_form_errors_as_json(form):
        """Convert form errors to JSON format"""
        import json
        
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = [str(e) for e in error_list]
        
        return json.dumps(errors)
    
    @staticmethod
    def get_field_errors(form, field_name):
        """Get errors for specific field"""
        if field_name in form.errors:
            return list(form.errors[field_name])
        return []
    
    @staticmethod
    def has_form_errors(form):
        """Check if form has any errors"""
        return bool(form.errors)


class FormHelperMixin:
    """Mixin for form helper methods"""
    
    def add_css_class(self, field_name, css_class):
        """Add CSS class to form field"""
        if field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = css_class
    
    def add_placeholder(self, field_name, placeholder):
        """Add placeholder text to form field"""
        if field_name in self.fields:
            self.fields[field_name].widget.attrs['placeholder'] = placeholder
    
    def add_help_text(self, field_name, help_text):
        """Add help text to form field"""
        if field_name in self.fields:
            self.fields[field_name].help_text = help_text
    
    def make_field_required(self, field_name):
        """Make field required"""
        if field_name in self.fields:
            self.fields[field_name].required = True
    
    def make_field_optional(self, field_name):
        """Make field optional"""
        if field_name in self.fields:
            self.fields[field_name].required = False
    
    def add_bootstrap_classes(self):
        """Add Bootstrap classes to all form fields"""
        for field_name in self.fields:
            widget = self.fields[field_name].widget
            current_class = widget.attrs.get('class', '')
            widget.attrs['class'] = f'{current_class} form-control'.strip()


class BootstrapFormMixin:
    """Mixin to add Bootstrap styling to forms"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            widget = field.widget
            widget.attrs['class'] = 'form-control'
            
            # Add specific classes based on widget type
            if hasattr(widget, 'input_type'):
                if widget.input_type in ['checkbox', 'radio']:
                    widget.attrs['class'] = 'form-check-input'
            
            # Add required attribute
            if field.required:
                widget.attrs['required'] = True


class FormErrorDisplay:
    """Helper for displaying form errors"""
    
    @staticmethod
    def get_form_error_html(form):
        """Get HTML for form errors"""
        if not form.errors:
            return ''
        
        html = '<div class="alert alert-danger" role="alert"><ul>'
        
        for field, errors in form.errors.items():
            for error in errors:
                html += f'<li>{field}: {error}</li>'
        
        html += '</ul></div>'
        return html
    
    @staticmethod
    def get_field_error_html(form, field_name):
        """Get HTML for specific field errors"""
        errors = FormValidationHelper.get_field_errors(form, field_name)
        
        if not errors:
            return ''
        
        html = '<div class="invalid-feedback" style="display: block;">'
        
        for error in errors:
            html += f'<span>{error}</span><br>'
        
        html += '</div>'
        return html


class AjaxFormHelper:
    """Helper for AJAX form submission"""
    
    @staticmethod
    def get_form_data_for_ajax(form):
        """Get form data in format suitable for AJAX"""
        import json
        
        data = {}
        for field_name, field in form.fields.items():
            if field_name in form.data:
                data[field_name] = form.data[field_name]
        
        return json.dumps(data)
    
    @staticmethod
    def create_ajax_response(success, message, data=None):
        """Create AJAX response object"""
        import json
        
        response = {
            'success': success,
            'message': message
        }
        
        if data:
            response['data'] = data
        
        return json.dumps(response)
    
    @staticmethod
    def create_error_response(form):
        """Create AJAX response with form errors"""
        import json
        
        return json.dumps({
            'success': False,
            'message': 'Form validation failed',
            'errors': {field: list(errors) for field, errors in form.errors.items()}
        })
