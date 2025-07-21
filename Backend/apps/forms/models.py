"""
Form models for KPA ERP system.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Form(models.Model):
    """
    Model representing a form template.
    """
    FORM_TYPES = [
        ('contact', _('Contact Form')),
        ('feedback', _('Feedback Form')),
        ('survey', _('Survey Form')),
        ('application', _('Application Form')),
        ('other', _('Other')),
    ]
    
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    form_type = models.CharField(_('form type'), max_length=20, choices=FORM_TYPES, default='other')
    is_active = models.BooleanField(_('is active'), default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_forms'
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')
        db_table = 'forms'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class FormField(models.Model):
    """
    Model representing fields within a form.
    """
    FIELD_TYPES = [
        ('text', _('Text')),
        ('email', _('Email')),
        ('number', _('Number')),
        ('tel', _('Phone')),
        ('url', _('URL')),
        ('textarea', _('Textarea')),
        ('select', _('Select')),
        ('radio', _('Radio')),
        ('checkbox', _('Checkbox')),
        ('date', _('Date')),
        ('time', _('Time')),
        ('datetime', _('DateTime')),
        ('file', _('File')),
    ]
    
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(_('label'), max_length=200)
    field_type = models.CharField(_('field type'), max_length=20, choices=FIELD_TYPES)
    placeholder = models.CharField(_('placeholder'), max_length=200, blank=True)
    help_text = models.TextField(_('help text'), blank=True)
    is_required = models.BooleanField(_('is required'), default=False)
    order = models.PositiveIntegerField(_('order'), default=0)
    options = models.JSONField(_('options'), blank=True, null=True, help_text=_('For select, radio, checkbox fields'))
    validation_rules = models.JSONField(_('validation rules'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Form Field')
        verbose_name_plural = _('Form Fields')
        db_table = 'form_fields'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.form.title} - {self.label}"


class FormSubmission(models.Model):
    """
    Model representing a form submission.
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('reviewed', _('Reviewed')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    ]
    
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='submissions')
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='form_submissions',
        null=True,
        blank=True
    )
    submission_data = models.JSONField(_('submission data'))
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(_('submitted at'), auto_now_add=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='reviewed_submissions',
        null=True,
        blank=True
    )
    reviewed_at = models.DateTimeField(_('reviewed at'), null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('Form Submission')
        verbose_name_plural = _('Form Submissions')
        db_table = 'form_submissions'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.form.title} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"


class WheelSpecification(models.Model):
    """
    Model for wheel specification forms with detailed measurement data.
    """
    # Form metadata
    form_number = models.CharField(_('form number'), max_length=50, unique=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wheel_specifications'
    )
    submitted_date = models.DateField(_('submitted date'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # Wheel measurement fields
    tread_diameter_new = models.CharField(
        _('tread diameter new'), 
        max_length=100, 
        help_text='e.g., 915 (900-1000)'
    )
    last_shop_issue_size = models.CharField(
        _('last shop issue size'), 
        max_length=100, 
        help_text='e.g., 837 (800-900)'
    )
    condemning_dia = models.CharField(
        _('condemning diameter'), 
        max_length=100, 
        help_text='e.g., 825 (800-900)'
    )
    wheel_gauge = models.CharField(
        _('wheel gauge'), 
        max_length=100, 
        help_text='e.g., 1600 (+2,-1)'
    )
    variation_same_axle = models.CharField(
        _('variation same axle'), 
        max_length=50, 
        help_text='e.g., 0.5'
    )
    variation_same_bogie = models.CharField(
        _('variation same bogie'), 
        max_length=50, 
        help_text='e.g., 5'
    )
    variation_same_coach = models.CharField(
        _('variation same coach'), 
        max_length=50, 
        help_text='e.g., 13'
    )
    wheel_profile = models.CharField(
        _('wheel profile'), 
        max_length=100, 
        help_text='e.g., 29.4 Flange Thickness'
    )
    intermediate_wwp = models.CharField(
        _('intermediate WWP'), 
        max_length=100, 
        help_text='e.g., 20 TO 28'
    )
    bearing_seat_diameter = models.CharField(
        _('bearing seat diameter'), 
        max_length=100, 
        help_text='e.g., 130.043 TO 130.068'
    )
    roller_bearing_outer_dia = models.CharField(
        _('roller bearing outer diameter'), 
        max_length=100, 
        help_text='e.g., 280 (+0.0/-0.035)'
    )
    roller_bearing_bore_dia = models.CharField(
        _('roller bearing bore diameter'), 
        max_length=100, 
        help_text='e.g., 130 (+0.0/-0.025)'
    )
    roller_bearing_width = models.CharField(
        _('roller bearing width'), 
        max_length=100, 
        help_text='e.g., 93 (+0/-0.250)'
    )
    axle_box_housing_bore_dia = models.CharField(
        _('axle box housing bore diameter'), 
        max_length=100, 
        help_text='e.g., 280 (+0.030/+0.052)'
    )
    wheel_disc_width = models.CharField(
        _('wheel disc width'), 
        max_length=100, 
        help_text='e.g., 127 (+4/-0)'
    )
    
    # Status field
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=[
            ('saved', 'Saved'),
            ('submitted', 'Submitted'),
            ('reviewed', 'Reviewed'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='saved'
    )
    
    class Meta:
        verbose_name = _('Wheel Specification')
        verbose_name_plural = _('Wheel Specifications')
        db_table = 'wheel_specifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['form_number']),
            models.Index(fields=['submitted_by']),
            models.Index(fields=['submitted_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.form_number


class BogieChecksheet(models.Model):
    """
    Model for bogie checksheet forms with detailed inspection data.
    """
    # Form metadata
    form_number = models.CharField(_('form number'), max_length=50, unique=True)
    inspection_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bogie_checksheets'
    )
    inspection_date = models.DateField(_('inspection date'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # Bogie Details
    bogie_no = models.CharField(_('bogie number'), max_length=50)
    maker_year_built = models.CharField(_('maker/year built'), max_length=100)
    incoming_div_and_date = models.CharField(_('incoming division and date'), max_length=200)
    deficit_components = models.TextField(_('deficit components'), blank=True, default='None')
    date_of_ioh = models.DateField(_('date of IOH'))
    
    # Bogie Checksheet - Condition assessments
    bogie_frame_condition = models.CharField(
        _('bogie frame condition'),
        max_length=50,
        choices=[
            ('Good', 'Good'),
            ('Fair', 'Fair'),
            ('Poor', 'Poor'),
            ('Damaged', 'Damaged'),
        ]
    )
    bolster = models.CharField(
        _('bolster'),
        max_length=50,
        choices=[
            ('Good', 'Good'),
            ('Fair', 'Fair'),
            ('Poor', 'Poor'),
            ('Damaged', 'Damaged'),
        ]
    )
    bolster_suspension_bracket = models.CharField(
        _('bolster suspension bracket'),
        max_length=50,
        choices=[
            ('Good', 'Good'),
            ('Fair', 'Fair'),
            ('Poor', 'Poor'),
            ('Cracked', 'Cracked'),
            ('Damaged', 'Damaged'),
        ]
    )
    lower_spring_seat = models.CharField(
        _('lower spring seat'),
        max_length=50,
        choices=[
            ('Good', 'Good'),
            ('Fair', 'Fair'),
            ('Poor', 'Poor'),
            ('Damaged', 'Damaged'),
        ]
    )
    axle_guide = models.CharField(
        _('axle guide'),
        max_length=50,
        choices=[
            ('Good', 'Good'),
            ('Fair', 'Fair'),
            ('Worn', 'Worn'),
            ('Damaged', 'Damaged'),
        ]
    )
    
    # BMBC Checksheet - BMBC component conditions
    cylinder_body = models.CharField(
        _('cylinder body'),
        max_length=50,
        choices=[
            ('GOOD', 'Good'),
            ('FAIR', 'Fair'),
            ('WORN OUT', 'Worn Out'),
            ('DAMAGED', 'Damaged'),
        ]
    )
    piston_trunnion = models.CharField(
        _('piston trunnion'),
        max_length=50,
        choices=[
            ('GOOD', 'Good'),
            ('FAIR', 'Fair'),
            ('WORN OUT', 'Worn Out'),
            ('DAMAGED', 'Damaged'),
        ]
    )
    adjusting_tube = models.CharField(
        _('adjusting tube'),
        max_length=50,
        choices=[
            ('GOOD', 'Good'),
            ('FAIR', 'Fair'),
            ('WORN OUT', 'Worn Out'),
            ('DAMAGED', 'Damaged'),
        ]
    )
    plunger_spring = models.CharField(
        _('plunger spring'),
        max_length=50,
        choices=[
            ('GOOD', 'Good'),
            ('FAIR', 'Fair'),
            ('WORN OUT', 'Worn Out'),
            ('DAMAGED', 'Damaged'),
        ]
    )
    
    # Status field
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=[
            ('saved', 'Saved'),
            ('submitted', 'Submitted'),
            ('reviewed', 'Reviewed'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='saved'
    )
    
    class Meta:
        verbose_name = _('Bogie Checksheet')
        verbose_name_plural = _('Bogie Checksheets')
        db_table = 'bogie_checksheets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['form_number']),
            models.Index(fields=['inspection_by']),
            models.Index(fields=['inspection_date']),
            models.Index(fields=['bogie_no']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.form_number} - {self.bogie_no}" 