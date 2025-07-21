"""
User data serializers for the users app.
"""
from ninja import Schema, Field
from datetime import date, datetime
from typing import Optional


class UserSerializer(Schema):
    """Serializer for basic user information."""
    id: int = Field(..., description="Unique user identifier", example=123)
    phone_number: str = Field(..., description="User's phone number (username)", example="+1234567890")
    first_name: str = Field(..., description="User's first name", example="John")
    last_name: str = Field(..., description="User's last name", example="Doe")
    email: Optional[str] = Field(None, description="User's email address", example="john.doe@example.com")
    is_active: bool = Field(..., description="Whether the user account is active", example=True)
    date_joined: datetime = Field(..., description="Date and time when user joined", example="2025-01-15T10:30:00Z")
    
    class Config:
        from_attributes = True


class UserDetailSerializer(Schema):
    """Serializer for detailed user information."""
    id: int = Field(..., description="Unique user identifier", example=123)
    phone_number: str = Field(..., description="User's phone number (username)", example="+1234567890")
    first_name: str = Field(..., description="User's first name", example="John")
    last_name: str = Field(..., description="User's last name", example="Doe")
    email: Optional[str] = Field(None, description="User's email address", example="john.doe@example.com")
    bio: Optional[str] = Field(None, description="User biography/description", example="Railway maintenance engineer with 10 years experience")
    date_of_birth: Optional[date] = Field(None, description="User's date of birth", example="1990-01-15")
    is_active: bool = Field(..., description="Whether the user account is active", example=True)
    is_staff: bool = Field(..., description="Whether the user has admin privileges", example=False)
    date_joined: datetime = Field(..., description="Date and time when user joined", example="2025-01-15T10:30:00Z")
    last_login: Optional[datetime] = Field(None, description="Last login date and time", example="2025-01-16T09:15:00Z")
    
    # Address fields
    address_line_1: Optional[str] = Field(None, description="Primary address line", example="123 Main Street")
    address_line_2: Optional[str] = Field(None, description="Secondary address line", example="Apartment 4B")
    city: Optional[str] = Field(None, description="City", example="Mumbai")
    state: Optional[str] = Field(None, description="State/Province", example="Maharashtra")
    postal_code: Optional[str] = Field(None, description="Postal/ZIP code", example="400001")
    country: Optional[str] = Field(None, description="Country", example="India")
    
    # Business fields
    employee_id: Optional[str] = Field(None, description="Employee identification number", example="EMP001")
    department: Optional[str] = Field(None, description="Department/Division", example="Mechanical Engineering")
    position: Optional[str] = Field(None, description="Job position/title", example="Senior Maintenance Engineer")
    
    class Config:
        from_attributes = True


class UserListSerializer(Schema):
    """Serializer for user list view."""
    id: int = Field(..., description="Unique user identifier", example=123)
    phone_number: str = Field(..., description="User's phone number", example="+1234567890")
    first_name: str = Field(..., description="User's first name", example="John")
    last_name: str = Field(..., description="User's last name", example="Doe")
    email: Optional[str] = Field(None, description="User's email address", example="john.doe@example.com")
    department: Optional[str] = Field(None, description="Department/Division", example="Mechanical Engineering")
    position: Optional[str] = Field(None, description="Job position/title", example="Senior Maintenance Engineer")
    is_active: bool = Field(..., description="Whether the user account is active", example=True)
    
    class Config:
        from_attributes = True


class UserCreateSerializer(Schema):
    """Serializer for creating new users (admin only)."""
    phone_number: str = Field(..., description="Unique phone number (used as username)", example="+1234567890")
    password: str = Field(..., description="Initial password (minimum 8 characters)", example="temppassword123")
    first_name: str = Field(..., description="User's first name", example="John")
    last_name: str = Field(..., description="User's last name", example="Doe")
    email: Optional[str] = Field(None, description="Email address", example="john.doe@example.com")
    is_staff: bool = Field(default=False, description="Grant admin privileges", example=False)
    is_active: bool = Field(default=True, description="Activate user account immediately", example=True)
    employee_id: Optional[str] = Field(None, description="Employee identification number", example="EMP001")
    department: Optional[str] = Field(None, description="Department/Division", example="Mechanical Engineering")
    position: Optional[str] = Field(None, description="Job position/title", example="Senior Maintenance Engineer") 