"""
Django admin configuration for the users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for the User model with phone number authentication.
    """
    
    # Fields to display in the user list
    list_display = (
        'phone_number', 
        'first_name', 
        'last_name', 
        'email',
        'department',
        'position',
        'is_active', 
        'is_staff', 
        'date_joined'
    )
    
    # Fields to filter by in the admin sidebar
    list_filter = (
        'is_staff', 
        'is_superuser', 
        'is_active', 
        'date_joined',
        'department',
        'position'
    )
    
    # Fields to search by
    search_fields = ('phone_number', 'first_name', 'last_name', 'email', 'employee_id')
    
    # Default ordering
    ordering = ('-date_joined',)
    
    # Fields for the user detail/edit form
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 
                'last_name', 
                'email', 
                'bio',
                'date_of_birth',
                'profile_picture'
            )
        }),
        (_('Address'), {
            'fields': (
                'address_line_1',
                'address_line_2', 
                'city', 
                'state', 
                'postal_code', 
                'country'
            ),
            'classes': ('collapse',)
        }),
        (_('Work Information'), {
            'fields': (
                'employee_id',
                'department', 
                'position', 
                'manager'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number', 
                'password1', 
                'password2',
                'first_name',
                'last_name',
                'email',
                'is_active',
                'is_staff'
            ),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('date_joined', 'last_login')
    
    # Filter horizontal for many-to-many fields
    filter_horizontal = ('groups', 'user_permissions')
    
    def get_queryset(self, request):
        """
        Optimize query by selecting related fields.
        """
        return super().get_queryset(request).select_related('manager') 