/**
 * Frontend form utilities and enhancement functions
 * Provides form validation, password strength checking, and field interactions
 */

// Form Validation Helper
const FormValidation = {
    /**
     * Validate email format
     * @param {string} email - Email address to validate
     * @returns {boolean} - True if valid email
     */
    isValidEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    /**
     * Validate required field
     * @param {string} value - Field value to validate
     * @returns {boolean} - True if field is not empty
     */
    isRequired: function(value) {
        return value.trim() !== '';
    },

    /**
     * Validate password strength
     * @param {string} password - Password to validate
     * @returns {object} - Strength level and feedback
     */
    checkPasswordStrength: function(password) {
        let strength = 0;
        const feedback = [];

        if (password.length >= 8) strength++;
        else feedback.push('At least 8 characters');

        if (password.length >= 12) strength++;
        else if (password.length >= 8) feedback.push('12+ characters recommended');

        if (/[a-z]/.test(password)) strength++;
        else feedback.push('Add lowercase letters');

        if (/[A-Z]/.test(password)) strength++;
        else feedback.push('Add uppercase letters');

        if (/[0-9]/.test(password)) strength++;
        else feedback.push('Add numbers');

        if (/[^a-zA-Z0-9]/.test(password)) strength++;
        else feedback.push('Add special characters');

        const levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
        const colors = ['danger', 'warning', 'warning', 'info', 'success', 'success'];

        return {
            level: levels[strength] || 'Very Weak',
            strength: strength,
            color: colors[strength] || 'danger',
            feedback: feedback
        };
    },

    /**
     * Validate form field
     * @param {HTMLElement} field - Form field element
     * @returns {boolean} - True if field is valid
     */
    validateField: function(field) {
        const value = field.value;
        let isValid = true;

        // Check if field is required
        if (field.hasAttribute('required')) {
            isValid = this.isRequired(value);
        }

        // Check email fields
        if (field.type === 'email' && value) {
            isValid = this.isValidEmail(value);
        }

        // Check password match for password confirmation fields
        if (field.classList.contains('password-confirm')) {
            const passwordField = document.querySelector('[name="password"]');
            if (passwordField) {
                isValid = field.value === passwordField.value;
            }
        }

        return isValid;
    }
};

// Password Strength Indicator
const PasswordStrengthIndicator = {
    /**
     * Initialize password strength indicator for password fields
     */
    init: function() {
        const passwordInputs = document.querySelectorAll('input[type="password"][name="password"]');
        
        passwordInputs.forEach(input => {
            // Create strength meter if it doesn't exist
            if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('password-strength-meter')) {
                const meter = document.createElement('div');
                meter.className = 'password-strength-meter mt-2';
                meter.innerHTML = `
                    <div class="progress" style="height: 5px;">
                        <div class="progress-bar" id="strength-bar-${input.id || 'password'}" style="width: 0%;"></div>
                    </div>
                    <small class="password-strength-text d-block mt-1"></small>
                `;
                input.parentNode.insertBefore(meter, input.nextSibling);
            }

            // Update strength on input
            input.addEventListener('input', () => {
                this.updateStrength(input);
            });
        });
    },

    /**
     * Update password strength display
     * @param {HTMLElement} input - Password input field
     */
    updateStrength: function(input) {
        const strength = FormValidation.checkPasswordStrength(input.value);
        const meterId = input.id || 'password';
        const strengthBar = document.querySelector(`#strength-bar-${meterId}`);
        const strengthText = input.parentNode.querySelector('.password-strength-text');

        if (strengthBar) {
            const width = (strength.strength / 6) * 100;
            strengthBar.style.width = width + '%';
            strengthBar.className = `progress-bar bg-${strength.color}`;
        }

        if (strengthText) {
            strengthText.innerHTML = `
                <strong>Strength:</strong> ${strength.level}
                ${strength.feedback.length > 0 ? '<br>' + strength.feedback.join(', ') : ''}
            `;
            strengthText.className = `password-strength-text d-block mt-1 text-${strength.color}`;
        }
    }
};

// Form Error Display
const FormErrorDisplay = {
    /**
     * Display field error
     * @param {HTMLElement} field - Form field
     * @param {string} message - Error message
     */
    showError: function(field, message) {
        // Remove existing error
        this.clearError(field);

        // Add error class to field
        field.classList.add('is-invalid');

        // Create and insert error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    },

    /**
     * Clear field error
     * @param {HTMLElement} field - Form field
     */
    clearError: function(field) {
        field.classList.remove('is-invalid');
        const errorMsg = field.parentNode.querySelector('.invalid-feedback');
        if (errorMsg) {
            errorMsg.remove();
        }
    },

    /**
     * Clear all form errors
     * @param {HTMLElement} form - Form element
     */
    clearAllErrors: function(form) {
        const fields = form.querySelectorAll('.is-invalid');
        fields.forEach(field => {
            this.clearError(field);
        });
    }
};

// Form Handler
const FormHandler = {
    /**
     * Initialize form handlers
     */
    init: function() {
        PasswordStrengthIndicator.init();
        this.setupFormValidation();
    },

    /**
     * Setup real-time form validation
     */
    setupFormValidation: function() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            // Validate on blur
            const fields = form.querySelectorAll('input, textarea, select');
            fields.forEach(field => {
                field.addEventListener('blur', () => {
                    const isValid = FormValidation.validateField(field);
                    if (!isValid && field.hasAttribute('required')) {
                        FormErrorDisplay.showError(field, 'This field is required');
                    } else {
                        FormErrorDisplay.clearError(field);
                    }
                });

                // Clear error on input
                field.addEventListener('input', () => {
                    if (field.classList.contains('is-invalid')) {
                        const isValid = FormValidation.validateField(field);
                        if (isValid) {
                            FormErrorDisplay.clearError(field);
                        }
                    }
                });
            });

            // Validate on submit
            form.addEventListener('submit', (e) => {
                FormErrorDisplay.clearAllErrors(form);
                let isFormValid = true;

                fields.forEach(field => {
                    const isValid = FormValidation.validateField(field);
                    if (!isValid && field.hasAttribute('required')) {
                        FormErrorDisplay.showError(field, 'This field is required');
                        isFormValid = false;
                    }
                });

                if (!isFormValid) {
                    e.preventDefault();
                }
            });
        });
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    FormHandler.init();
});
