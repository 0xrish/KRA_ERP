"""
Helper functions for KPA ERP system.
"""
import re
import string
import random
from typing import Optional


def generate_random_string(length: int = 10, include_digits: bool = True, include_symbols: bool = False) -> str:
    """
    Generate a random string of specified length.
    
    Args:
        length: Length of the string to generate
        include_digits: Whether to include digits
        include_symbols: Whether to include symbols
    
    Returns:
        Random string
    """
    characters = string.ascii_letters
    
    if include_digits:
        characters += string.digits
    
    if include_symbols:
        characters += '!@#$%^&*'
    
    return ''.join(random.choice(characters) for _ in range(length))


def format_phone_number(phone: str) -> str:
    """
    Format phone number to a consistent format.
    
    Args:
        phone: Raw phone number string
    
    Returns:
        Formatted phone number
    """
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # If it starts with +, keep it
    if cleaned.startswith('+'):
        return cleaned
    
    # If it's a 10-digit number, assume it needs +1
    if len(cleaned) == 10:
        return f'+1{cleaned}'
    
    # If it's 11 digits and starts with 1, add +
    if len(cleaned) == 11 and cleaned.startswith('1'):
        return f'+{cleaned}'
    
    return cleaned


def truncate_string(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length allowed
        suffix: Suffix to add when truncating
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def slugify(text: str) -> str:
    """
    Convert text to a URL-friendly slug.
    
    Args:
        text: Text to slugify
    
    Returns:
        Slugified string
    """
    # Convert to lowercase
    text = text.lower()
    
    # Replace spaces and special characters with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    
    # Remove leading/trailing hyphens
    return text.strip('-')


def mask_phone_number(phone: str) -> str:
    """
    Mask phone number for privacy (show only last 4 digits).
    
    Args:
        phone: Phone number to mask
    
    Returns:
        Masked phone number
    """
    if len(phone) <= 4:
        return phone
    
    return '*' * (len(phone) - 4) + phone[-4:]


def mask_email(email: str) -> str:
    """
    Mask email address for privacy.
    
    Args:
        email: Email to mask
    
    Returns:
        Masked email
    """
    if '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    
    if len(local) <= 2:
        masked_local = local
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    return f'{masked_local}@{domain}'


def calculate_age(birth_date) -> Optional[int]:
    """
    Calculate age from birth date.
    
    Args:
        birth_date: Date of birth
    
    Returns:
        Age in years or None if invalid date
    """
    if not birth_date:
        return None
    
    from datetime import date
    today = date.today()
    
    try:
        age = today.year - birth_date.year
        
        # Adjust if birthday hasn't occurred this year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        
        return age
    except (AttributeError, TypeError):
        return None


def get_client_ip(request) -> str:
    """
    Get client IP address from request.
    
    Args:
        request: Django request object
    
    Returns:
        Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return ip or 'unknown' 