/**
 * UI Interactions and utilities for PDFCrypto
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme from localStorage
    initializeTheme();
    
    // Initialize mobile menu functionality
    initializeMobileMenu();
    
    // Initialize file drag and drop enhancements
    initializeDragDropEnhancements();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
});

/**
 * Theme Management
 */
function initializeTheme() {
    // Theme is handled by Alpine.js, but we can add transitions
    document.documentElement.classList.add('transition-colors', 'duration-300');
}

/**
 * Mobile Menu Functionality
 */
function initializeMobileMenu() {
    const mobileMenuButton = document.querySelector('[data-mobile-menu-button]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            const isOpen = mobileMenu.classList.contains('show');
            
            if (isOpen) {
                mobileMenu.classList.remove('show');
                mobileMenu.classList.add('hide');
            } else {
                mobileMenu.classList.remove('hide');
                mobileMenu.classList.add('show');
            }
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenuButton.contains(event.target) && !mobileMenu.contains(event.target)) {
                mobileMenu.classList.remove('show');
                mobileMenu.classList.add('hide');
            }
        });
    }
}

/**
 * Enhanced Drag and Drop functionality
 */
function initializeDragDropEnhancements() {
    // Prevent default drag behaviors on the document
    document.addEventListener('dragover', function(e) {
        e.preventDefault();
    });
    
    document.addEventListener('dragleave', function(e) {
        e.preventDefault();
    });
    
    document.addEventListener('drop', function(e) {
        e.preventDefault();
    });
    
    // Add visual feedback for drag and drop areas
    const dropZones = document.querySelectorAll('[data-drop-zone]');
    
    dropZones.forEach(zone => {
        zone.addEventListener('dragenter', function(e) {
            e.preventDefault();
            this.classList.add('drag-active');
        });
        
        zone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            // Only remove class if we're leaving the drop zone entirely
            if (!this.contains(e.relatedTarget)) {
                this.classList.remove('drag-active');
            }
        });
        
        zone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-active');
        });
    });
}

/**
 * Form Validation Enhancements
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateInput(this);
            });
            
            input.addEventListener('input', function() {
                clearValidationError(this);
            });
        });
    });
}

function validateInput(input) {
    const value = input.value.trim();
    const isValid = input.checkValidity();
    
    clearValidationError(input);
    
    if (!isValid || value === '') {
        showValidationError(input, getValidationMessage(input));
        return false;
    }
    
    return true;
}

function showValidationError(input, message) {
    input.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    
    let errorElement = input.parentNode.querySelector('.validation-error');
    if (!errorElement) {
        errorElement = document.createElement('p');
        errorElement.className = 'validation-error text-sm text-red-600 dark:text-red-400 mt-1';
        input.parentNode.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

function clearValidationError(input) {
    input.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    
    const errorElement = input.parentNode.querySelector('.validation-error');
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

function getValidationMessage(input) {
    if (input.type === 'file') {
        return 'Please select a valid file.';
    } else if (input.type === 'password') {
        return 'Password is required.';
    } else {
        return 'This field is required.';
    }
}

/**
 * Keyboard Shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + D for dark mode toggle
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            toggleDarkMode();
        }
        
        // Escape key to close modals/alerts
        if (e.key === 'Escape') {
            closeAlerts();
        }
        
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.querySelector('form:focus-within');
            if (activeForm) {
                e.preventDefault();
                activeForm.requestSubmit();
            }
        }
    });
}

function toggleDarkMode() {
    const html = document.documentElement;
    const isDark = html.classList.contains('dark');
    
    if (isDark) {
        html.classList.remove('dark');
        localStorage.setItem('darkMode', 'false');
    } else {
        html.classList.add('dark');
        localStorage.setItem('darkMode', 'true');
    }
}

function closeAlerts() {
    const alerts = document.querySelectorAll('[data-alert]');
    alerts.forEach(alert => {
        alert.style.display = 'none';
    });
}

/**
 * Utility Functions
 */

/**
 * Show notification toast
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, error, info, warning)
 * @param {number} duration - Duration in milliseconds
 */
function showNotification(message, type = 'info', duration = 5000) {
    const notification = createNotificationElement(message, type);
    document.body.appendChild(notification);
    
    // Trigger animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Auto remove
    setTimeout(() => {
        removeNotification(notification);
    }, duration);
    
    // Manual close button
    const closeButton = notification.querySelector('[data-close]');
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            removeNotification(notification);
        });
    }
}

function createNotificationElement(message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 max-w-sm w-full bg-white dark:bg-gray-800 border-l-4 rounded-lg shadow-lg transform translate-x-full transition-transform duration-300 z-50 notification-toast`;
    
    const colorClasses = {
        success: 'border-green-500 text-green-800 dark:text-green-200',
        error: 'border-red-500 text-red-800 dark:text-red-200',
        warning: 'border-yellow-500 text-yellow-800 dark:text-yellow-200',
        info: 'border-blue-500 text-blue-800 dark:text-blue-200'
    };
    
    notification.classList.add(...colorClasses[type].split(' '));
    
    const icons = {
        success: '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>',
        error: '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>',
        warning: '<path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>',
        info: '<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>'
    };
    
    notification.innerHTML = `
        <div class="flex p-4">
            <div class="flex-shrink-0">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    ${icons[type]}
                </svg>
            </div>
            <div class="ml-3 flex-1">
                <p class="text-sm font-medium">${message}</p>
            </div>
            <div class="ml-4 flex-shrink-0 flex">
                <button data-close class="inline-flex text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 focus:outline-none">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        </div>
    `;
    
    return notification;
}

function removeNotification(notification) {
    notification.classList.remove('show');
    notification.classList.add('translate-x-full');
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

/**
 * Loading state management
 */
function showLoading(element, text = 'Loading...') {
    if (!element) return;
    
    const originalContent = element.innerHTML;
    element.setAttribute('data-original-content', originalContent);
    element.disabled = true;
    
    element.innerHTML = `
        <div class="flex items-center justify-center">
            <div class="loading-spinner mr-2"></div>
            <span>${text}</span>
        </div>
    `;
}

function hideLoading(element) {
    if (!element) return;
    
    const originalContent = element.getAttribute('data-original-content');
    if (originalContent) {
        element.innerHTML = originalContent;
        element.removeAttribute('data-original-content');
    }
    element.disabled = false;
}

/**
 * File size formatting
 */
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success', 2000);
        return true;
    } catch (err) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showNotification('Copied to clipboard!', 'success', 2000);
            return true;
        } catch (err) {
            document.body.removeChild(textArea);
            showNotification('Failed to copy to clipboard', 'error', 3000);
            return false;
        }
    }
}

/**
 * Add custom styles for loading spinner and transitions
 */
const customStyles = `
    .notification-toast.show {
        transform: translateX(0);
    }
    
    .drag-active {
        border-color: #3b82f6 !important;
        background-color: rgba(59, 130, 246, 0.05) !important;
    }
    
    .dark .drag-active {
        background-color: rgba(59, 130, 246, 0.1) !important;
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .pulse-slow {
        animation: pulse 2s infinite;
    }
`;

// Add custom styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = customStyles;
document.head.appendChild(styleSheet);

// Export functions for use in other scripts
window.PDFCryptoUtils = {
    showNotification,
    showLoading,
    hideLoading,
    formatBytes,
    debounce,
    copyToClipboard,
    toggleDarkMode
};