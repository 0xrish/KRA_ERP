"""
Shared constants for KPA ERP system.
"""

# Phone number constants
PHONE_NUMBER_REGEX = r'^\+?1?\d{9,15}$'
PHONE_NUMBER_MIN_LENGTH = 9
PHONE_NUMBER_MAX_LENGTH = 17

# User constants
DEFAULT_USER_AVATAR = '/static/images/default-avatar.png'
MAX_PROFILE_PICTURE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_FORMATS = ['JPEG', 'JPG', 'PNG', 'GIF']

# Form constants
MAX_FORM_FIELDS = 50
MAX_FIELD_OPTIONS = 100
MAX_SUBMISSION_DATA_SIZE = 10 * 1024 * 1024  # 10MB

# API Response constants
SUCCESS_MESSAGES = {
    'USER_CREATED': 'User created successfully',
    'USER_UPDATED': 'User updated successfully',
    'USER_DELETED': 'User deleted successfully',
    'PASSWORD_CHANGED': 'Password changed successfully',
    'FORM_CREATED': 'Form created successfully',
    'FORM_UPDATED': 'Form updated successfully',
    'FORM_DELETED': 'Form deleted successfully',
    'SUBMISSION_CREATED': 'Form submitted successfully',
}

ERROR_MESSAGES = {
    'INVALID_CREDENTIALS': 'Invalid phone number or password',
    'USER_NOT_FOUND': 'User not found',
    'USER_INACTIVE': 'User account is disabled',
    'PERMISSION_DENIED': 'Permission denied',
    'INVALID_TOKEN': 'Invalid or expired token',
    'PHONE_EXISTS': 'User with this phone number already exists',
    'EMAIL_EXISTS': 'User with this email already exists',
    'FORM_NOT_FOUND': 'Form not found',
    'INVALID_FORM_DATA': 'Invalid form data provided',
}

# Pagination constants
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# File upload constants
UPLOAD_PATHS = {
    'PROFILE_PICTURES': 'profile_pictures/',
    'FORM_ATTACHMENTS': 'form_attachments/',
    'DOCUMENTS': 'documents/',
}

# Status choices
USER_STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('suspended', 'Suspended'),
]

FORM_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('archived', 'Archived'),
]

SUBMISSION_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('reviewed', 'Reviewed'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

# Date formats
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT = '%H:%M:%S'

# Cache keys
CACHE_KEYS = {
    'USER_PROFILE': 'user_profile_{user_id}',
    'FORM_DETAILS': 'form_details_{form_id}',
    'FORM_LIST': 'form_list_{page}',
}

# Cache timeouts (in seconds)
CACHE_TIMEOUTS = {
    'SHORT': 300,      # 5 minutes
    'MEDIUM': 1800,    # 30 minutes
    'LONG': 3600,      # 1 hour
    'VERY_LONG': 86400, # 24 hours
} 