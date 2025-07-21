"""
Authentication-related serializers for the users app.
"""
from typing import Dict, Any
from ninja import Schema, Field
from pydantic import validator
from datetime import date
from typing import Optional


class LoginSerializer(Schema):
    """Serializer for user login."""
    phone_number: str = Field(..., description="User's phone number (used as username)", example="+1234567890")
    password: str = Field(..., description="User's password", example="securepassword123")
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not v:
            raise ValueError('Phone number is required')
        # Basic phone number validation
        if len(v) < 9 or len(v) > 17:
            raise ValueError('Phone number must be between 9 and 17 characters')
        return v


class RegisterSerializer(Schema):
    """Serializer for user registration."""
    phone_number: str = Field(..., description="Unique phone number (used as username)", example="+1234567890")
    password: str = Field(..., description="Password (minimum 8 characters)", example="securepassword123")
    confirm_password: str = Field(..., description="Password confirmation (must match password)", example="securepassword123")
    first_name: str = Field(..., description="User's first name", example="John")
    last_name: str = Field(..., description="User's last name", example="Doe")
    email: Optional[str] = Field(None, description="Optional email address", example="john.doe@example.com")
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not v:
            raise ValueError('Phone number is required')
        if len(v) < 9 or len(v) > 17:
            raise ValueError('Phone number must be between 9 and 17 characters')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password is required')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('first_name')
    def validate_first_name(cls, v):
        if not v or not v.strip():
            raise ValueError('First name is required')
        return v.strip()
    
    @validator('last_name')
    def validate_last_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Last name is required')
        return v.strip()


class UserProfileSerializer(Schema):
    """Serializer for user profile updates."""
    first_name: Optional[str] = Field(None, description="User's first name", example="John")
    last_name: Optional[str] = Field(None, description="User's last name", example="Doe")
    email: Optional[str] = Field(None, description="Email address", example="john.doe@example.com")
    bio: Optional[str] = Field(None, description="User biography/description", example="Railway maintenance engineer with 10 years experience")
    date_of_birth: Optional[date] = Field(None, description="Date of birth", example="1990-01-15")
    address_line_1: Optional[str] = Field(None, description="Primary address line", example="123 Main Street")
    address_line_2: Optional[str] = Field(None, description="Secondary address line (optional)", example="Apartment 4B")
    city: Optional[str] = Field(None, description="City", example="Mumbai")
    state: Optional[str] = Field(None, description="State/Province", example="Maharashtra")
    postal_code: Optional[str] = Field(None, description="Postal/ZIP code", example="400001")
    country: Optional[str] = Field(None, description="Country", example="India")
    department: Optional[str] = Field(None, description="Department/Division", example="Mechanical Engineering")
    position: Optional[str] = Field(None, description="Job position/title", example="Senior Maintenance Engineer")
    
    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v


class ChangePasswordSerializer(Schema):
    """Serializer for changing password."""
    old_password: str = Field(..., description="Current password", example="oldpassword123")
    new_password: str = Field(..., description="New password (minimum 8 characters)", example="newpassword123")
    confirm_new_password: str = Field(..., description="Confirm new password (must match new_password)", example="newpassword123")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if not v:
            raise ValueError('New password is required')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('confirm_new_password')
    def validate_confirm_new_password(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class TokenResponseSerializer(Schema):
    """Serializer for JWT token response."""
    access_token: str = Field(..., description="JWT access token for API authentication", example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...")
    refresh_token: str = Field(..., description="JWT refresh token for obtaining new access tokens", example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...")
    token_type: str = Field(default="Bearer", description="Token type (always 'Bearer')", example="Bearer")
    expires_in: int = Field(..., description="Access token expiration time in seconds", example=3600)


class MessageResponseSerializer(Schema):
    """Serializer for simple message responses."""
    message: str = Field(..., description="Response message", example="Operation completed successfully")
    success: bool = Field(default=True, description="Operation success status", example=True) 