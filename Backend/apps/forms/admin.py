"""
Read-only Django admin configuration for the forms app.
All form operations should be done through the API endpoints.
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import Form, FormField, FormSubmission, WheelSpecification, BogieChecksheet


class FormFieldInline(admin.TabularInline):
    """Read-only inline admin for form fields."""
    model = FormField
    extra = 0
    can_delete = False
    readonly_fields = [
        'label', 'field_type', 'placeholder', 'help_text', 
        'is_required', 'order', 'options', 'validation_rules'
    ]
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    """Read-only admin configuration for Form model."""
    list_display = (
        'title', 
        'form_type', 
        'is_active', 
        'created_by', 
        'field_count',
        'submission_count',
        'created_at'
    )
    list_filter = ('form_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = (
        'title', 'description', 'form_type', 'is_active',
        'created_by', 'created_at', 'updated_at'
    )
    inlines = [FormFieldInline]
    
    def field_count(self, obj):
        """Display number of fields in the form."""
        return obj.fields.count()
    field_count.short_description = 'Fields'
    
    def submission_count(self, obj):
        """Display number of submissions for the form."""
        count = obj.submissions.count()
        if count > 0:
            return format_html(
                '<a href="/admin/forms/formsubmission/?form__id__exact={}" style="color: #417690;">{}</a>',
                obj.id, count
            )
        return count
    submission_count.short_description = 'Submissions'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    """Read-only admin configuration for FormSubmission model."""
    list_display = (
        'form',
        'submitted_by',
        'status',
        'submitted_at',
        'reviewed_by',
        'reviewed_at'
    )
    list_filter = ('status', 'submitted_at', 'form__form_type')
    search_fields = (
        'form__title', 
        'submitted_by__phone_number', 
        'submitted_by__first_name',
        'submitted_by__last_name'
    )
    ordering = ('-submitted_at',)
    readonly_fields = (
        'form', 'submitted_by', 'submission_data', 'status',
        'submitted_at', 'reviewed_by', 'reviewed_at', 'notes'
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WheelSpecification)
class WheelSpecificationAdmin(admin.ModelAdmin):
    """Read-only admin configuration for WheelSpecification model."""
    list_display = (
        'form_number',
        'submitted_by',
        'submitted_date',
        'status',
        'created_at'
    )
    list_filter = ('status', 'submitted_date', 'created_at')
    search_fields = (
        'form_number', 
        'submitted_by__phone_number', 
        'submitted_by__first_name',
        'submitted_by__last_name'
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'form_number', 'submitted_by', 'submitted_date', 'status',
        'tread_diameter_new', 'last_shop_issue_size', 'condemning_dia',
        'wheel_gauge', 'variation_same_axle', 'variation_same_bogie',
        'variation_same_coach', 'wheel_profile', 'intermediate_wwp',
        'bearing_seat_diameter', 'roller_bearing_outer_dia',
        'roller_bearing_bore_dia', 'roller_bearing_width',
        'axle_box_housing_bore_dia', 'wheel_disc_width',
        'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('Form Information', {
            'fields': ('form_number', 'submitted_by', 'submitted_date', 'status')
        }),
        ('Wheel Measurements', {
            'fields': (
                'tread_diameter_new',
                'last_shop_issue_size', 
                'condemning_dia',
                'wheel_gauge',
                'wheel_profile',
                'wheel_disc_width'
            )
        }),
        ('Variations', {
            'fields': (
                'variation_same_axle',
                'variation_same_bogie',
                'variation_same_coach'
            )
        }),
        ('Bearing Specifications', {
            'fields': (
                'bearing_seat_diameter',
                'roller_bearing_outer_dia',
                'roller_bearing_bore_dia',
                'roller_bearing_width',
                'axle_box_housing_bore_dia'
            )
        }),
        ('Additional Data', {
            'fields': ('intermediate_wwp',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BogieChecksheet)
class BogieChecksheetAdmin(admin.ModelAdmin):
    """Read-only admin configuration for BogieChecksheet model."""
    list_display = (
        'form_number',
        'bogie_no',
        'inspection_by',
        'inspection_date',
        'status',
        'created_at'
    )
    list_filter = ('status', 'inspection_date', 'created_at')
    search_fields = (
        'form_number',
        'bogie_no',
        'inspection_by__phone_number',
        'inspection_by__first_name',
        'inspection_by__last_name'
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'form_number', 'inspection_by', 'inspection_date', 'status',
        'bogie_no', 'maker_year_built', 'incoming_div_and_date',
        'deficit_components', 'date_of_ioh', 'bogie_frame_condition',
        'bolster', 'bolster_suspension_bracket', 'lower_spring_seat',
        'axle_guide', 'cylinder_body', 'piston_trunnion',
        'adjusting_tube', 'plunger_spring', 'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('Form Information', {
            'fields': ('form_number', 'inspection_by', 'inspection_date', 'status')
        }),
        ('Bogie Details', {
            'fields': (
                'bogie_no',
                'maker_year_built',
                'incoming_div_and_date',
                'deficit_components',
                'date_of_ioh'
            )
        }),
        ('Bogie Condition Assessment', {
            'fields': (
                'bogie_frame_condition',
                'bolster',
                'bolster_suspension_bracket',
                'lower_spring_seat',
                'axle_guide'
            )
        }),
        ('BMBC Assessment', {
            'fields': (
                'cylinder_body',
                'piston_trunnion',
                'adjusting_tube',
                'plunger_spring'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


# Add custom admin site styling
admin.site.site_header = "KPA ERP Forms Administration"
admin.site.site_title = "KPA ERP Forms Admin"
admin.site.index_title = "Forms Management (Read-Only - Use API for modifications)" 