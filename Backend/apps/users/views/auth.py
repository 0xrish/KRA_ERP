"""
Authentication views for the users app using Django Ninja.
"""
from typing import List
from django.contrib.auth import authenticate
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth

from apps.users.models import User
from apps.users.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserCreateSerializer,
    ChangePasswordSerializer,
    TokenResponseSerializer,
    MessageResponseSerializer,
)

router = Router()

@router.post("/register", response=TokenResponseSerializer, auth=None, tags=["Authentication"])
def register(request, payload: RegisterSerializer):
    """
    Register a new user with phone number and password.
    
    **Description:**
    Create a new user account using phone number as the unique identifier.
    Upon successful registration, returns JWT tokens for immediate authentication.
    
    **Request Example:**
    ```json
    {
      "phone_number": "+1234567890",
      "password": "securepassword123",
      "confirm_password": "securepassword123",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com"
    }
    ```
    
    **Validation Rules:**
    - Phone number must be unique and 9-17 characters long
    - Password must be at least 8 characters long
    - Passwords must match
    - First name and last name are required
    - Email is optional but must be valid format if provided
    
    **Success Response:**
    Returns JWT access and refresh tokens with 1-hour expiration.
    
    **Error Responses:**
    - `400`: User already exists, validation errors
    - `500`: Server error during registration
    """
    # Check if user already exists
    if User.objects.filter(phone_number=payload.phone_number).exists():
        return {"detail": "User with this phone number already exists"}, 400
    
    # Check if email already exists (if provided)
    if payload.email and User.objects.filter(email=payload.email).exists():
        return {"detail": "User with this email already exists"}, 400
    
    try:
        with transaction.atomic():
            # Create new user
            user = User.objects.create_user(
                phone_number=payload.phone_number,
                password=payload.password,
                first_name=payload.first_name,
                last_name=payload.last_name,
                email=payload.email if payload.email else None,
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return {
                "access_token": str(access_token),
                "refresh_token": str(refresh),
                "token_type": "Bearer",
                "expires_in": 3600,  # 1 hour
            }
    except Exception as e:
        return {"detail": f"Registration failed: {str(e)}"}, 500


@router.post("/login", response=TokenResponseSerializer, auth=None, tags=["Authentication"])
def login(request, payload: LoginSerializer):
    """
    Login user with phone number and password.
    
    **Description:**
    Authenticate a user using their phone number (username) and password.
    Returns JWT tokens for API access upon successful authentication.
    
    **Request Example:**
    ```json
    {
      "phone_number": "+1234567890",
      "password": "securepassword123"
    }
    ```
    
    **Authentication Flow:**
    1. Validates phone number and password
    2. Checks if user account is active
    3. Generates JWT access and refresh tokens
    4. Returns tokens with expiration information
    
    **Token Usage:**
    Use the access token in the Authorization header for subsequent API calls:
    ```
    Authorization: Bearer <access_token>
    ```
    
    **Error Responses:**
    - `401`: Invalid credentials or inactive account
    """
    # Authenticate user
    user = authenticate(
        request,
        username=payload.phone_number,
        password=payload.password
    )
    
    if not user:
        return {"detail": "Invalid phone number or password"}, 401
    
    if not user.is_active:
        return {"detail": "User account is disabled"}, 401
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    
    return {
        "access_token": str(access_token),
        "refresh_token": str(refresh),
        "token_type": "Bearer",
        "expires_in": 3600,  # 1 hour
    }


@router.post("/refresh", response=TokenResponseSerializer, auth=None, tags=["Authentication"])
def refresh_token(request, refresh_token: str):
    """
    Refresh access token using refresh token.
    
    **Description:**
    Obtain a new access token using a valid refresh token.
    This endpoint allows extending user sessions without requiring re-login.
    
    **Request:**
    Send the refresh token as a string parameter.
    
    **Usage Example:**
    ```
    POST /api/users/refresh
    Content-Type: application/json
    
    "your_refresh_token_here"
    ```
    
    **Token Lifecycle:**
    - Access tokens expire in 1 hour
    - Refresh tokens have longer expiration
    - Use this endpoint before access token expires
    - Both tokens are rotated on refresh for security
    
    **Error Responses:**
    - `401`: Invalid or expired refresh token
    """
    try:
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token
        
        return {
            "access_token": str(access_token),
            "refresh_token": str(refresh),
            "token_type": "Bearer",
            "expires_in": 3600,  # 1 hour
        }
    except Exception as e:
        return {"detail": "Invalid refresh token"}, 401


@router.get("/profile", response=UserDetailSerializer, auth=JWTAuth(), tags=["Profile"])
def get_profile(request):
    """
    Get current user's profile information.
    
    **Description:**
    Retrieve complete profile information for the currently authenticated user.
    Includes personal details, address information, and business-related fields.
    
    **Authentication:**
    Requires valid JWT token in Authorization header.
    
    **Response Includes:**
    - Basic information (name, phone, email)
    - Personal details (bio, date of birth)
    - Address information (complete address fields)
    - Business information (employee ID, department, position)
    - Account status and timestamps
    
    **Usage:**
    ```
    GET /api/users/profile
    Authorization: Bearer <your_access_token>
    ```
    
    **Error Responses:**
    - `401`: Authentication required or invalid token
    """
    return request.auth


@router.put("/profile", response=UserDetailSerializer, auth=JWTAuth(), tags=["Profile"])
def update_profile(request, payload: UserProfileSerializer):
    """
    Update current user's profile information.
    
    **Description:**
    Update profile information for the currently authenticated user.
    All fields are optional - only provided fields will be updated.
    
    **Request Example:**
    ```json
    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "bio": "Senior Railway Maintenance Engineer",
      "date_of_birth": "1990-01-15",
      "address_line_1": "123 Main Street",
      "city": "Mumbai",
      "state": "Maharashtra",
      "postal_code": "400001",
      "department": "Mechanical Engineering",
      "position": "Senior Engineer"
    }
    ```
    
    **Updateable Fields:**
    - Personal info: name, email, bio, date of birth
    - Address: complete address information
    - Business: department, position (if allowed)
    
    **Error Responses:**
    - `401`: Authentication required
    - `400`: Validation errors (e.g., invalid email format)
    """
    user = request.auth
    
    # Update user fields
    for field, value in payload.dict(exclude_unset=True).items():
        if hasattr(user, field) and value is not None:
            setattr(user, field, value)
    
    user.save()
    return user


@router.post("/change-password", response=MessageResponseSerializer, auth=JWTAuth(), tags=["Profile"])
def change_password(request, payload: ChangePasswordSerializer):
    """
    Change current user's password.
    
    **Description:**
    Securely change the password for the currently authenticated user.
    Requires verification of the current password before setting a new one.
    
    **Request Example:**
    ```json
    {
      "old_password": "currentpassword123",
      "new_password": "newpassword123",
      "confirm_new_password": "newpassword123"
    }
    ```
    
    **Security Requirements:**
    - Must provide correct current password
    - New password must be at least 8 characters long
    - New password confirmation must match
    - All existing tokens remain valid (consider logout/re-login for security)
    
    **Process:**
    1. Validates current password
    2. Validates new password requirements
    3. Updates password securely (hashed)
    4. Returns success confirmation
    
    **Error Responses:**
    - `401`: Authentication required
    - `400`: Invalid current password or validation errors
    """
    user = request.auth
    
    # Check old password
    if not user.check_password(payload.old_password):
        return {"detail": "Invalid old password"}, 400
    
    # Set new password
    user.set_password(payload.new_password)
    user.save()
    
    return {
        "message": "Password changed successfully",
        "success": True
    }


@router.get("/users", response=List[UserListSerializer], auth=JWTAuth(), tags=["User Management"])
def list_users(request):
    """
    Get list of all users (admin only).
    
    **Description:**
    Retrieve a list of all users in the system. This endpoint is restricted to admin users only.
    Returns a simplified view of user information optimized for listing/management purposes.
    
    **Admin Permission Required:**
    Only users with `is_staff=True` can access this endpoint.
    
    **Response Includes:**
    - Basic user information (ID, name, phone, email)
    - Business information (department, position)
    - Account status (active/inactive)
    - Excludes sensitive information (passwords, detailed personal data)
    
    **Ordering:**
    Results are ordered by registration date (newest first).
    
    **Usage:**
    ```
    GET /api/users/users
    Authorization: Bearer <admin_access_token>
    ```
    
    **Error Responses:**
    - `401`: Authentication required
    - `403`: Permission denied (non-admin user)
    """
    user = request.auth
    if not user.is_staff:
        return {"detail": "Permission denied"}, 403
    
    users = User.objects.all().order_by('-date_joined')
    return users


@router.get("/users/{user_id}", response=UserDetailSerializer, auth=JWTAuth(), tags=["User Management"])
def get_user(request, user_id: int):
    """
    Get specific user details (admin only or own profile).
    
    **Description:**
    Retrieve detailed information for a specific user. Users can access their own profile,
    while admin users can access any user's profile.
    
    **Access Control:**
    - Any user can view their own profile (user_id matches their ID)
    - Admin users (is_staff=True) can view any user's profile
    - Regular users cannot view other users' profiles
    
    **Response Includes:**
    Complete user profile with personal, address, and business information.
    
    **Usage Examples:**
    ```
    GET /api/users/users/123  # Admin viewing any user
    GET /api/users/users/456  # User viewing own profile (if user_id = 456)
    Authorization: Bearer <access_token>
    ```
    
    **Error Responses:**
    - `401`: Authentication required
    - `403`: Permission denied (trying to view other user without admin rights)
    - `404`: User not found
    """
    current_user = request.auth
    
    # Allow users to view their own profile
    if current_user.id == user_id:
        return current_user
    
    # Check if user is admin
    if not current_user.is_staff:
        return {"detail": "Permission denied"}, 403
    
    user = get_object_or_404(User, id=user_id)
    return user


@router.post("/users", response=UserDetailSerializer, auth=JWTAuth(), tags=["User Management"])
def create_user(request, payload: UserCreateSerializer):
    """
    Create a new user (admin only).
    
    **Description:**
    Create a new user account with full profile information. This endpoint is restricted
    to admin users only and allows setting all user fields including staff status.
    
    **Admin Permission Required:**
    Only users with `is_staff=True` can create new users.
    
    **Request Example:**
    ```json
    {
      "phone_number": "+1234567890",
      "password": "temppassword123",
      "first_name": "Jane",
      "last_name": "Smith",
      "email": "jane.smith@example.com",
      "is_staff": false,
      "is_active": true,
      "employee_id": "EMP002",
      "department": "Operations",
      "position": "Field Engineer"
    }
    ```
    
    **Features:**
    - Sets initial password (user should change on first login)
    - Can assign admin privileges (is_staff)
    - Can set business information (employee_id, department, position)
    - Account is active by default but can be created as inactive
    
    **Error Responses:**
    - `401`: Authentication required
    - `403`: Permission denied (non-admin user)
    - `400`: Validation errors or user already exists
    - `500`: Server error during creation
    """
    current_user = request.auth
    if not current_user.is_staff:
        return {"detail": "Permission denied"}, 403
    
    # Check if user already exists
    if User.objects.filter(phone_number=payload.phone_number).exists():
        return {"detail": "User with this phone number already exists"}, 400
    
    if payload.email and User.objects.filter(email=payload.email).exists():
        return {"detail": "User with this email already exists"}, 400
    
    try:
        with transaction.atomic():
            user = User.objects.create_user(
                phone_number=payload.phone_number,
                password=payload.password,
                first_name=payload.first_name,
                last_name=payload.last_name,
                email=payload.email,
                is_staff=payload.is_staff,
                is_active=payload.is_active,
                employee_id=payload.employee_id,
                department=payload.department,
                position=payload.position,
            )
            return user
    except Exception as e:
        return {"detail": f"User creation failed: {str(e)}"}, 500


@router.put("/users/{user_id}", response=UserDetailSerializer, auth=JWTAuth(), tags=["User Management"])
def update_user(request, user_id: int, payload: UserProfileSerializer):
    """
    Update user profile (admin only or own profile).
    
    **Description:**
    Update user profile information. Users can update their own profile,
    while admin users can update any user's profile.
    
    **Access Control:**
    - Any user can update their own profile (user_id matches their ID)
    - Admin users (is_staff=True) can update any user's profile
    - Regular users cannot update other users' profiles
    
    **Request Example:**
    ```json
    {
      "first_name": "Jane",
      "last_name": "Smith",
      "email": "jane.smith@newdomain.com",
      "department": "Engineering",
      "position": "Lead Engineer"
    }
    ```
    
    **Updateable Fields:**
    All fields in UserProfileSerializer are optional and can be updated.
    Only provided fields will be modified.
    
    **Note:**
    Passwords cannot be updated through this endpoint. Use the change-password
    endpoint for password updates.
    
    **Error Responses:**
    - `401`: Authentication required
    - `403`: Permission denied (trying to update other user without admin rights)
    - `404`: User not found
    - `400`: Validation errors
    """
    current_user = request.auth
    
    # Allow users to update their own profile
    if current_user.id == user_id:
        user = current_user
    else:
        # Check if user is admin
        if not current_user.is_staff:
            return {"detail": "Permission denied"}, 403
        user = get_object_or_404(User, id=user_id)
    
    # Update user fields
    for field, value in payload.dict(exclude_unset=True).items():
        if hasattr(user, field) and value is not None:
            setattr(user, field, value)
    
    user.save()
    return user


@router.delete("/users/{user_id}", response=MessageResponseSerializer, auth=JWTAuth(), tags=["User Management"])
def delete_user(request, user_id: int):
    """
    Delete/deactivate user (admin only).
    
    **Description:**
    Deactivate a user account by setting is_active=False. This is a soft delete
    that preserves user data while preventing login and API access.
    
    **Admin Permission Required:**
    Only users with `is_staff=True` can deactivate users.
    
    **Security Restrictions:**
    - Admin users cannot delete their own account
    - This prevents accidental lockout from the system
    - Data is preserved for audit and recovery purposes
    
    **Soft Delete Behavior:**
    - Sets user.is_active = False
    - User data remains in database
    - User cannot login or access API
    - Can be reactivated by updating is_active = True
    
    **Usage:**
    ```
    DELETE /api/users/users/123
    Authorization: Bearer <admin_access_token>
    ```
    
    **Alternative:**
    For permanent deletion or complete user management, use Django admin interface.
    
    **Error Responses:**
    - `401`: Authentication required
    - `403`: Permission denied (non-admin user)
    - `404`: User not found
    - `400`: Cannot delete own account
    """
    current_user = request.auth
    if not current_user.is_staff:
        return {"detail": "Permission denied"}, 403
    
    if current_user.id == user_id:
        return {"detail": "Cannot delete your own account"}, 400
    
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    
    return {
        "message": "User deactivated successfully",
        "success": True
    } 