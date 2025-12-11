/**
 * MWECAU ICT Club - Main JavaScript Utilities
 */

// Utility object for common functions
const MWECAU = {
    // Show notification
    notify: function(message, type = 'info', duration = 5000) {
        const alertClass = `alert-${type}`;
        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        const alertContainer = document.querySelector('[data-alert-container]') || 
                             document.body;
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = alertHtml;
        alertContainer.insertBefore(tempDiv.firstElementChild, alertContainer.firstChild);
        
        if (duration > 0) {
            setTimeout(() => {
                const alert = document.querySelector('.alert');
                if (alert) {
                    alert.remove();
                }
            }, duration);
        }
    },
    
    // Success notification
    success: function(message) {
        this.notify(message, 'success');
    },
    
    // Error notification
    error: function(message) {
        this.notify(message, 'danger');
    },
    
    // Warning notification
    warning: function(message) {
        this.notify(message, 'warning');
    },
    
    // Info notification
    info: function(message) {
        this.notify(message, 'info');
    },
    
    // Confirm dialog
    confirm: function(message, callback) {
        if (window.confirm(message)) {
            callback(true);
        } else {
            callback(false);
        }
    },
    
    // API call wrapper
    fetch: function(url, options = {}) {
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        // Add CSRF token if it exists
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            defaultOptions.headers['X-CSRFToken'] = csrfToken.value;
        }
        
        const finalOptions = { ...defaultOptions, ...options };
        
        return fetch(url, finalOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('Fetch error:', error);
                throw error;
            });
    },
    
    // Format date
    formatDate: function(date) {
        if (typeof date === 'string') {
            date = new Date(date);
        }
        
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        return date.toLocaleDateString('en-US', options);
    },
    
    // Format time
    formatTime: function(date) {
        if (typeof date === 'string') {
            date = new Date(date);
        }
        
        const options = { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true
        };
        return date.toLocaleTimeString('en-US', options);
    },
    
    // Format datetime
    formatDateTime: function(date) {
        return `${this.formatDate(date)} ${this.formatTime(date)}`;
    },
    
    // Countdown timer
    countdown: function(targetDate, elementId) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        const timer = setInterval(() => {
            const now = new Date().getTime();
            const target = new Date(targetDate).getTime();
            const distance = target - now;
            
            if (distance < 0) {
                clearInterval(timer);
                element.textContent = 'Deadline passed';
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            let text = '';
            if (days > 0) text += `${days}d `;
            if (hours > 0) text += `${hours}h `;
            if (minutes > 0) text += `${minutes}m `;
            text += `${seconds}s`;
            
            element.textContent = text;
        }, 1000);
    },
    
    // Debounce function
    debounce: function(func, delay = 300) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    },
    
    // Search with debounce
    setupSearch: function(searchInputId, searchFunction) {
        const searchInput = document.getElementById(searchInputId);
        if (!searchInput) return;
        
        const debouncedSearch = this.debounce(searchFunction, 300);
        searchInput.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
    },
    
    // Image lazy loading
    setupLazyLoading: function() {
        const images = document.querySelectorAll('img[data-src]');
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => observer.observe(img));
        } else {
            // Fallback for older browsers
            images.forEach(img => {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            });
        }
    },
    
    // Toggle element visibility
    toggleElement: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = element.style.display === 'none' ? 'block' : 'none';
        }
    },
    
    // Show element
    showElement: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'block';
        }
    },
    
    // Hide element
    hideElement: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'none';
        }
    },
    
    // Scroll to element
    scrollToElement: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    },
    
    // Copy to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.success('Copied to clipboard!');
        }).catch(() => {
            this.error('Failed to copy');
        });
    },
    
    // Get CSRF token
    getCsrfToken: function() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    },
    
    // Initialize tooltips
    initTooltips: function() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    },
    
    // Initialize popovers
    initPopovers: function() {
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    },
};

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers
    MWECAU.initTooltips();
    MWECAU.initPopovers();
    
    // Setup lazy loading
    MWECAU.setupLazyLoading();
});
