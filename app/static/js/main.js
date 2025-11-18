// ===== Theme Management =====
$(document).ready(function() {
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    // Theme toggle button
    $('#themeToggle').click(function() {
        const currentTheme = $('body').attr('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    });
});

function setTheme(theme) {
    $('body').attr('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // Update icon
    if (theme === 'dark') {
        $('#themeIcon').removeClass('bi-moon-fill').addClass('bi-sun-fill');
    } else {
        $('#themeIcon').removeClass('bi-sun-fill').addClass('bi-moon-fill');
    }
}

// ===== Alert/Toast Functions =====
function showAlert(message, type = 'success', duration = 5000) {
    const alertId = 'alert-' + Date.now();
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert" id="${alertId}">
            <i class="bi bi-${getAlertIcon(type)}"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('#alertContainer').append(alertHtml);
    
    // Auto dismiss after duration
    if (duration > 0) {
        setTimeout(function() {
            $('#' + alertId).alert('close');
        }, duration);
    }
}

function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle-fill',
        'danger': 'exclamation-triangle-fill',
        'warning': 'exclamation-circle-fill',
        'info': 'info-circle-fill'
    };
    return icons[type] || 'info-circle-fill';
}

function showError(message) {
    showAlert(message, 'danger', 7000);
}

function showSuccess(message) {
    showAlert(message, 'success', 5000);
}

function showInfo(message) {
    showAlert(message, 'info', 5000);
}

function showWarning(message) {
    showAlert(message, 'warning', 6000);
}

// ===== Loading Spinner =====
function showLoading(elementId) {
    $(`#${elementId}`).show();
}

function hideLoading(elementId) {
    $(`#${elementId}`).hide();
}

// ===== API Helper Functions =====
function apiRequest(url, method = 'GET', data = null) {
    const options = {
        url: url,
        method: method,
        contentType: 'application/json',
        dataType: 'json'
    };
    
    if (data) {
        options.data = JSON.stringify(data);
    }
    
    return $.ajax(options);
}

function apiGet(url) {
    return apiRequest(url, 'GET');
}

function apiPost(url, data) {
    return apiRequest(url, 'POST', data);
}

function apiPut(url, data) {
    return apiRequest(url, 'PUT', data);
}

function apiDelete(url) {
    return apiRequest(url, 'DELETE');
}

// ===== Format Functions =====
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatBoolean(value, trueText = 'Sim', falseText = 'Não') {
    return value ? trueText : falseText;
}

// ===== Active Navigation Highlight =====
$(document).ready(function() {
    const currentPath = window.location.pathname;
    $('.nav-link').each(function() {
        const linkPath = $(this).attr('href');
        if (linkPath === currentPath) {
            $(this).addClass('active');
        }
    });
});

// ===== Modal Helper Functions =====
function openModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
}

function closeModal(modalId) {
    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
    if (modal) {
        modal.hide();
    }
}

// ===== Form Validation Helper =====
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        form.reportValidity();
        return false;
    }
    return true;
}

// ===== Debounce Function for Search =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}


