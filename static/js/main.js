// Main JavaScript file for extrackr

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeConfirmDialogs();
    initializeAutoDismissAlerts();
});

// Tooltip initialization
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const element = event.target;
    const tooltipText = element.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip absolute bg-gray-800 text-white px-2 py-1 rounded text-sm z-50';
    tooltip.textContent = tooltipText;
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    element.tooltip = tooltip;
}

function hideTooltip(event) {
    const element = event.target;
    if (element.tooltip) {
        element.tooltip.remove();
        element.tooltip = null;
    }
}

// Confirmation dialogs for destructive actions
function initializeConfirmDialogs() {
    const confirmElements = document.querySelectorAll('[data-confirm]');
    confirmElements.forEach(element => {
        element.addEventListener('click', function(event) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });
}

// Auto-dismiss alerts after 5 seconds
function initializeAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.5s ease';
                setTimeout(() => alert.remove(), 500);
            }
        }, 5000);
    });
}

// Utility functions
const Utils = {
    // Format currency
    formatCurrency: function(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },
    
    // Format date
    formatDate: function(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Show loading spinner
    showLoading: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '<div class="spinner"></div>';
        }
    },
    
    // Hide loading spinner
    hideLoading: function(elementId, content) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = content;
        }
    }
};

// Chart utilities
const ChartUtils = {
    // Default layout for all charts
    getDefaultLayout: function() {
        return {
            showlegend: true,
            legend: {
                orientation: 'h',
                y: -0.2
            },
            margin: { t: 30, r: 30, b: 60, l: 60 },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
                family: 'Inter, system-ui, sans-serif',
                size: 12
            }
        };
    },
    
    // Default configuration for all charts
    getDefaultConfig: function() {
        return {
            responsive: true,
            displayModeBar: false
        };
    },
    
    // Common color palette
    colors: {
        primary: '#3B82F6',
        secondary: '#1E40AF',
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
        info: '#06B6D4',
        income: '#10B981',
        expense: '#EF4444'
    }
};

// Form utilities
const FormUtils = {
    // Validate form
    validateForm: function(formId) {
        const form = document.getElementById(formId);
        if (!form) return false;
        
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.showFieldError(field, 'This field is required');
                isValid = false;
            } else {
                this.clearFieldError(field);
            }
        });
        
        return isValid;
    },
    
    // Show field error
    showFieldError: function(field, message) {
        this.clearFieldError(field);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-red-600 text-sm mt-1 field-error';
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
        field.classList.add('border-red-500');
    },
    
    // Clear field error
    clearFieldError: function(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        field.classList.remove('border-red-500');
    },
    
    // Serialize form data
    serializeForm: function(formId) {
        const form = document.getElementById(formId);
        if (!form) return {};
        
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    }
};

// AJAX utilities
const AjaxUtils = {
    // Make AJAX request
    request: function(options) {
        const defaults = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };
        
        const config = Object.assign({}, defaults, options);
        
        if (config.method.toUpperCase() !== 'GET' && !config.headers['X-CSRFToken']) {
            const csrfToken = this.getCsrfToken();
            if (csrfToken) {
                config.headers['X-CSRFToken'] = csrfToken;
            }
        }
        
        return fetch(config.url, config)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('AJAX request failed:', error);
                throw error;
            });
    },
    
    // Get CSRF token
    getCsrfToken: function() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : null;
    }
};

// Local storage utilities
const StorageUtils = {
    // Set item with expiration
    setItem: function(key, value, expirationHours = 24) {
        const item = {
            value: value,
            expiration: Date.now() + (expirationHours * 60 * 60 * 1000)
        };
        localStorage.setItem(key, JSON.stringify(item));
    },
    
    // Get item with expiration check
    getItem: function(key) {
        const itemStr = localStorage.getItem(key);
        if (!itemStr) return null;
        
        const item = JSON.parse(itemStr);
        if (Date.now() > item.expiration) {
            localStorage.removeItem(key);
            return null;
        }
        
        return item.value;
    },
    
    // Remove item
    removeItem: function(key) {
        localStorage.removeItem(key);
    },
    
    // Clear all storage
    clear: function() {
        localStorage.clear();
    }
};

// Export utilities for use in other scripts
window.extrackr = {
    Utils,
    ChartUtils,
    FormUtils,
    AjaxUtils,
    StorageUtils
};