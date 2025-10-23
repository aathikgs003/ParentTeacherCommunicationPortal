// Form validation specific functions

// Validate login form
function validateLoginForm() {
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    let isValid = true;

    if (!username.value.trim()) {
        showFieldError(username, 'Username is required');
        isValid = false;
    } else {
        hideFieldError(username);
    }

    if (!password.value) {
        showFieldError(password, 'Password is required');
        isValid = false;
    } else {
        hideFieldError(password);
    }

    return isValid;
}

// Validate registration form
function validateRegistrationForm() {
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const role = document.getElementById('role');
    let isValid = true;

    // Username validation
    if (!username.value.trim()) {
        showFieldError(username, 'Username is required');
        isValid = false;
    } else if (username.value.length < 3) {
        showFieldError(username, 'Username must be at least 3 characters');
        isValid = false;
    } else {
        hideFieldError(username);
    }

    // Email validation
    if (!email.value.trim()) {
        showFieldError(email, 'Email is required');
        isValid = false;
    } else if (!isValidEmail(email.value)) {
        showFieldError(email, 'Please enter a valid email address');
        isValid = false;
    } else {
        hideFieldError(email);
    }

    // Password validation
    if (!password.value) {
        showFieldError(password, 'Password is required');
        isValid = false;
    } else if (password.value.length < 6) {
        showFieldError(password, 'Password must be at least 6 characters');
        isValid = false;
    } else {
        hideFieldError(password);
    }

    // Role validation
    if (!role.value) {
        showFieldError(role, 'Please select a role');
        isValid = false;
    } else {
        hideFieldError(role);
    }

    return isValid;
}

// Validate announcement form
function validateAnnouncementForm() {
    const title = document.getElementById('title');
    const content = document.getElementById('content');
    let isValid = true;

    if (!title.value.trim()) {
        showFieldError(title, 'Title is required');
        isValid = false;
    } else {
        hideFieldError(title);
    }

    if (!content.value.trim()) {
        showFieldError(content, 'Content is required');
        isValid = false;
    } else {
        hideFieldError(content);
    }

    return isValid;
}

// Validate message form
function validateMessageForm() {
    const recipientId = document.getElementById('recipient_id');
    const subject = document.getElementById('subject');
    const content = document.getElementById('content');
    let isValid = true;

    if (!recipientId.value) {
        showFieldError(recipientId, 'Please select a recipient');
        isValid = false;
    } else {
        hideFieldError(recipientId);
    }

    if (!subject.value.trim()) {
        showFieldError(subject, 'Subject is required');
        isValid = false;
    } else {
        hideFieldError(subject);
    }

    if (!content.value.trim()) {
        showFieldError(content, 'Message content is required');
        isValid = false;
    } else {
        hideFieldError(content);
    }

    return isValid;
}

// Validate report form
function validateReportForm() {
    const studentId = document.getElementById('student_id');
    const title = document.getElementById('title');
    const content = document.getElementById('content');
    let isValid = true;

    if (!studentId.value) {
        showFieldError(studentId, 'Please select a student');
        isValid = false;
    } else {
        hideFieldError(studentId);
    }

    if (!title.value.trim()) {
        showFieldError(title, 'Report title is required');
        isValid = false;
    } else {
        hideFieldError(title);
    }

    if (!content.value.trim()) {
        showFieldError(content, 'Report content is required');
        isValid = false;
    } else {
        hideFieldError(content);
    }

    return isValid;
}

// Validate attendance form
function validateAttendanceForm() {
    const studentId = document.getElementById('student_id');
    const date = document.getElementById('date');
    const status = document.getElementById('status');
    let isValid = true;

    if (!studentId.value) {
        showFieldError(studentId, 'Please select a student');
        isValid = false;
    } else {
        hideFieldError(studentId);
    }

    if (!date.value) {
        showFieldError(date, 'Date is required');
        isValid = false;
    } else {
        hideFieldError(date);
    }

    if (!status.value) {
        showFieldError(status, 'Please select attendance status');
        isValid = false;
    } else {
        hideFieldError(status);
    }

    return isValid;
}

// Helper functions
function showFieldError(field, message) {
    hideFieldError(field);
    field.style.borderColor = '#dc3545';
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '0.9rem';
    errorDiv.style.marginTop = '5px';
    field.parentNode.insertBefore(errorDiv, field.nextSibling);
}

function hideFieldError(field) {
    field.style.borderColor = '#ddd';
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Attach validation to forms on page load
document.addEventListener('DOMContentLoaded', function() {
    // Login form
    const loginForm = document.querySelector('form[action*="login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            if (!validateLoginForm()) {
                event.preventDefault();
            }
        });
    }

    // Registration form
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            if (!validateRegistrationForm()) {
                event.preventDefault();
            }
        });
    }

    // Announcement form
    const announcementForm = document.querySelector('form[action*="announcements"]');
    if (announcementForm) {
        announcementForm.addEventListener('submit', function(event) {
            if (!validateAnnouncementForm()) {
                event.preventDefault();
            }
        });
    }

    // Message forms
    const messageForms = document.querySelectorAll('form[action*="message"]');
    messageForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!validateMessageForm()) {
                event.preventDefault();
            }
        });
    });

    // Report form
    const reportForm = document.querySelector('form[action*="upload_report"]');
    if (reportForm) {
        reportForm.addEventListener('submit', function(event) {
            if (!validateReportForm()) {
                event.preventDefault();
            }
        });
    }

    // Attendance form
    const attendanceForm = document.querySelector('form[action*="attendance"]');
    if (attendanceForm) {
        attendanceForm.addEventListener('submit', function(event) {
            if (!validateAttendanceForm()) {
                event.preventDefault();
            }
        });
    }
});
