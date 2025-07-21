"""
Custom validators for KPA ERP system.
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .constants import PHONE_NUMBER_REGEX, ALLOWED_IMAGE_FORMATS, MAX_PROFILE_PICTURE_SIZE


def validate_phone_number(phone: str) -> None:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
    
    Raises:
        ValidationError: If phone number is invalid
    """
    if not re.match(PHONE_NUMBER_REGEX, phone):
        raise ValidationError(
            _('Phone number must be in format: +1234567890 (9-15 digits with optional + prefix)')
        )


def validate_image_file(file) -> None:
    """
    Validate uploaded image file.
    
    Args:
        file: Uploaded file object
    
    Raises:
        ValidationError: If file is invalid
    """
    # Check file size
    if file.size > MAX_PROFILE_PICTURE_SIZE:
        raise ValidationError(
            _('File size cannot exceed 5MB')
        )
    
    # Check file format
    try:
        from PIL import Image
        image = Image.open(file)
        
        if image.format not in ALLOWED_IMAGE_FORMATS:
            raise ValidationError(
                _('Only JPEG, PNG, and GIF images are allowed')
            )
        
        # Verify it's actually an image
        image.verify()
        
    except Exception:
        raise ValidationError(
            _('Invalid image file')
        )


def validate_json_field(value) -> None:
    """
    Validate JSON field content.
    
    Args:
        value: JSON value to validate
    
    Raises:
        ValidationError: If JSON is invalid
    """
    import json
    
    if value is None:
        return
    
    try:
        if isinstance(value, str):
            json.loads(value)
    except json.JSONDecodeError:
        raise ValidationError(
            _('Invalid JSON format')
        )


def validate_password_strength(password: str) -> None:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
    
    Raises:
        ValidationError: If password is too weak
    """
    if len(password) < 8:
        raise ValidationError(
            _('Password must be at least 8 characters long')
        )
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            _('Password must contain at least one uppercase letter')
        )
    
    if not re.search(r'[a-z]', password):
        raise ValidationError(
            _('Password must contain at least one lowercase letter')
        )
    
    if not re.search(r'\d', password):
        raise ValidationError(
            _('Password must contain at least one digit')
        )


def validate_employee_id(employee_id: str) -> None:
    """
    Validate employee ID format.
    
    Args:
        employee_id: Employee ID to validate
    
    Raises:
        ValidationError: If employee ID is invalid
    """
    # Example: EMP001, EMP-001, etc.
    pattern = r'^[A-Z]{2,4}-?\d{3,6}$'
    
    if not re.match(pattern, employee_id.upper()):
        raise ValidationError(
            _('Employee ID must be in format: ABC123 or ABC-123')
        ) 