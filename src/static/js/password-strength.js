/**
 * Password Strength Checker
 * Validates password strength and provides real-time visual feedback
 * 
 * Requirements:
 * - Minimum 8 characters
 * - At least 1 uppercase letter
 * - At least 1 lowercase letter
 * - At least 1 digit
 * - At least 1 special character
 */

document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password-input');
    
    if (!passwordInput) {
        console.warn('Password input field not found');
        return;
    }
    
    // Create strength indicator HTML
    const strengthContainer = document.createElement('div');
    strengthContainer.className = 'password-strength-container mt-2';
    strengthContainer.innerHTML = `
        <div class="password-strength-bar">
            <div class="password-strength-fill" id="strengthFill"></div>
        </div>
        <div class="password-strength-text" id="strengthText">
            <small>Password strength: <span id="strengthLabel">Weak</span></small>
        </div>
        <div class="password-requirements mt-2">
            <small class="d-block">Password must contain:</small>
            <ul class="list-unstyled small ms-3">
                <li id="req-length"><i class="req-icon">✗</i> At least 8 characters</li>
                <li id="req-uppercase"><i class="req-icon">✗</i> Uppercase letter (A-Z)</li>
                <li id="req-lowercase"><i class="req-icon">✗</i> Lowercase letter (a-z)</li>
                <li id="req-digit"><i class="req-icon">✗</i> Digit (0-9)</li>
                <li id="req-special"><i class="req-icon">✗</i> Special character (!@#$%^&*)</li>
            </ul>
        </div>
    `;
    
    // Insert after password input field
    passwordInput.parentNode.insertBefore(strengthContainer, passwordInput.nextSibling);
    
    const strengthFill = document.getElementById('strengthFill');
    const strengthLabel = document.getElementById('strengthLabel');
    const requirementElements = {
        'length': document.getElementById('req-length'),
        'uppercase': document.getElementById('req-uppercase'),
        'lowercase': document.getElementById('req-lowercase'),
        'digit': document.getElementById('req-digit'),
        'special': document.getElementById('req-special')
    };
    
    // Regular expressions for validation
    const patterns = {
        length: /.{8,}/,
        uppercase: /[A-Z]/,
        lowercase: /[a-z]/,
        digit: /\d/,
        special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/
    };
    
    function checkPasswordStrength(password) {
        const results = {
            length: patterns.length.test(password),
            uppercase: patterns.uppercase.test(password),
            lowercase: patterns.lowercase.test(password),
            digit: patterns.digit.test(password),
            special: patterns.special.test(password)
        };
        
        return results;
    }
    
    function updateRequirementUI(key, isMet) {
        const element = requirementElements[key];
        if (!element) return;
        
        const icon = element.querySelector('.req-icon');
        if (isMet) {
            element.classList.add('met');
            element.classList.remove('unmet');
            icon.textContent = '✓';
        } else {
            element.classList.add('unmet');
            element.classList.remove('met');
            icon.textContent = '✗';
        }
    }
    
    function updateStrengthUI(results) {
        const metRequirements = Object.values(results).filter(Boolean).length;
        let strength = 'Weak';
        let percentage = 0;
        let strengthClass = 'weak';
        
        // Calculate strength level
        if (metRequirements === 5) {
            strength = 'Strong';
            percentage = 100;
            strengthClass = 'strong';
        } else if (metRequirements >= 3) {
            strength = 'Good';
            percentage = 66;
            strengthClass = 'good';
        } else {
            strength = 'Weak';
            percentage = Math.max(20, metRequirements * 20);
            strengthClass = 'weak';
        }
        
        // Update strength bar
        strengthFill.style.width = percentage + '%';
        strengthFill.className = 'password-strength-fill ' + strengthClass;
        
        // Update strength label
        strengthLabel.textContent = strength;
        strengthLabel.className = 'strength-' + strengthClass;
        
        // Update individual requirements
        Object.keys(results).forEach(key => {
            updateRequirementUI(key, results[key]);
        });
    }
    
    // Listen to password input changes
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        
        if (password.length === 0) {
            // Reset UI when field is empty
            strengthFill.style.width = '0%';
            strengthFill.className = 'password-strength-fill weak';
            strengthLabel.textContent = 'Weak';
            strengthLabel.className = '';
            
            // Reset all requirements
            Object.values(requirementElements).forEach(element => {
                element.classList.remove('met', 'unmet');
                element.querySelector('.req-icon').textContent = '✗';
            });
        } else {
            const results = checkPasswordStrength(password);
            updateStrengthUI(results);
        }
    });
    
    // Optional: Validate on form submission
    const form = passwordInput.closest('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const password = passwordInput.value;
            const results = checkPasswordStrength(password);
            
            if (Object.values(results).filter(Boolean).length < 5) {
                e.preventDefault();
                alert('Password does not meet all strength requirements. Please review the requirements below.');
                passwordInput.focus();
            }
        });
    }
});
