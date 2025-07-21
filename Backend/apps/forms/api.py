"""
Django Ninja API endpoints for forms app.
"""
from typing import List, Optional
from datetime import date
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from .models import WheelSpecification, BogieChecksheet
from .schemas import (
    WheelSpecificationCreateSchema,
    WheelSpecificationCreateResponseSchema,
    WheelSpecificationListResponseSchema,
    WheelSpecificationFilterSchema,
    BogieChecksheetCreateSchema,
    BogieChecksheetCreateResponseSchema,
    BogieChecksheetListResponseSchema,
    BogieChecksheetFilterSchema,
    ErrorResponse,
    WheelSpecificationResponseDataSchema,
    WheelSpecificationFieldsSchema,
    BogieDetailsResponseSchema,
    BogieChecksheetResponseSchema,
    BMBCChecksheetResponseSchema,
    BogieChecksheetResponseDataSchema
)

User = get_user_model()
router = Router()


@router.post("/wheel-specifications", 
             response={201: WheelSpecificationCreateResponseSchema, 400: ErrorResponse},
             tags=["Wheel Specifications"],
             summary="Create Wheel Specification",
             description="Create a new wheel specification form with detailed measurement data")
def create_wheel_specification(request, payload: WheelSpecificationCreateSchema):
    """
    Create a new wheel specification with detailed measurement fields.
    
    This endpoint accepts wheel specification data including form metadata
    and all measurement fields required for wheel maintenance tracking.
    """
    try:
        # Get the user object from submitted_by ID
        try:
            user = User.objects.get(id=payload.submitted_by)
        except (User.DoesNotExist, ValueError):
            return 400, {
                "success": False,
                "message": "Invalid user ID provided",
                "errors": {"submitted_by": ["User not found"]}
            }
        
        # Check if form number already exists
        if WheelSpecification.objects.filter(form_number=payload.form_number).exists():
            return 400, {
                "success": False,
                "message": "Form number already exists",
                "errors": {"form_number": ["This form number is already in use"]}
            }
        
        # Create wheel specification
        wheel_spec = WheelSpecification.objects.create(
            form_number=payload.form_number,
            submitted_by=user,
            submitted_date=payload.submitted_date,
            tread_diameter_new=payload.fields.tread_diameter_new,
            last_shop_issue_size=payload.fields.last_shop_issue_size,
            condemning_dia=payload.fields.condemning_dia,
            wheel_gauge=payload.fields.wheel_gauge,
            variation_same_axle=payload.fields.variation_same_axle,
            variation_same_bogie=payload.fields.variation_same_bogie,
            variation_same_coach=payload.fields.variation_same_coach,
            wheel_profile=payload.fields.wheel_profile,
            intermediate_wwp=payload.fields.intermediate_wwp,
            bearing_seat_diameter=payload.fields.bearing_seat_diameter,
            roller_bearing_outer_dia=payload.fields.roller_bearing_outer_dia,
            roller_bearing_bore_dia=payload.fields.roller_bearing_bore_dia,
            roller_bearing_width=payload.fields.roller_bearing_width,
            axle_box_housing_bore_dia=payload.fields.axle_box_housing_bore_dia,
            wheel_disc_width=payload.fields.wheel_disc_width,
            status='submitted'
        )
        
        return 201, {
            "success": True,
            "message": "Wheel specification submitted successfully.",
            "data": {
                "formNumber": wheel_spec.form_number,
                "submittedBy": str(wheel_spec.submitted_by.id),
                "submittedDate": wheel_spec.submitted_date,
                "status": wheel_spec.status.title()
            }
        }
        
    except Exception as e:
        return 400, {
            "success": False,
            "message": f"Error creating wheel specification: {str(e)}",
            "errors": {"general": [str(e)]}
        }


@router.get("/wheel-specifications",
            response={200: WheelSpecificationListResponseSchema, 400: ErrorResponse},
            tags=["Wheel Specifications"],
            summary="Get Wheel Specifications",
            description="Retrieve wheel specifications with optional filtering")
def get_wheel_specifications(
    request,
    form_number: Optional[str] = None,
    submitted_by: Optional[str] = None,
    submitted_date: Optional[date] = None
):
    """
    Retrieve wheel specifications with optional filtering.
    
    Filter parameters:
    - formNumber: Filter by specific form number
    - submittedBy: Filter by user ID who submitted the form
    - submittedDate: Filter by submission date
    """
    try:
        # Start with all wheel specifications
        queryset = WheelSpecification.objects.all().select_related('submitted_by')
        filters_applied = False
        # Apply filters
        if form_number:
            queryset = queryset.filter(form_number__icontains=form_number)
            filters_applied = True
        if submitted_by:
            try:
                user = User.objects.get(id=submitted_by)
                queryset = queryset.filter(submitted_by=user)
                filters_applied = True
            except (User.DoesNotExist, ValueError):
                return 400, {
                    "success": False,
                    "message": "Invalid user ID provided",
                    "errors": {"submitted_by": ["User not found"]}
                }
        if submitted_date:
            queryset = queryset.filter(submitted_date=submitted_date)
            filters_applied = True
        # Convert to response format
        data = []
        for spec in queryset:
            # Create response data dict with proper structure
            response_data = {
                "formNumber": spec.form_number,
                "submittedBy": str(spec.submitted_by.id),
                "submittedDate": spec.submitted_date,
                "status": spec.status.title(),
                "fields": {
                    "treadDiameterNew": str(spec.tread_diameter_new),
                    "lastShopIssueSize": str(spec.last_shop_issue_size),
                    "condemningDia": str(spec.condemning_dia),
                    "wheelGauge": str(spec.wheel_gauge),
                    "variationSameAxle": str(spec.variation_same_axle),
                    "variationSameBogie": str(spec.variation_same_bogie),
                    "variationSameCoach": str(spec.variation_same_coach),
                    "wheelProfile": str(spec.wheel_profile),
                    "intermediateWWP": str(spec.intermediate_wwp),
                    "bearingSeatDiameter": str(spec.bearing_seat_diameter),
                    "rollerBearingOuterDia": str(spec.roller_bearing_outer_dia),
                    "rollerBearingBoreDia": str(spec.roller_bearing_bore_dia),
                    "rollerBearingWidth": str(spec.roller_bearing_width),
                    "axleBoxHousingBoreDia": str(spec.axle_box_housing_bore_dia),
                    "wheelDiscWidth": str(spec.wheel_disc_width)
                }
            }
            data.append(response_data)
        
        if filters_applied:
            message = "Filtered wheel specification forms fetched successfully."
        else:
            message = "All wheel specification forms fetched successfully."
        return 200, {
            "success": True,
            "message": message,
            "data": data
        }
        
    except Exception as e:
        return 400, {
            "success": False,
            "message": f"Error retrieving wheel specifications: {str(e)}",
            "errors": {"general": [str(e)]}
        }


@router.post("/bogie-checksheet",
             response={201: BogieChecksheetCreateResponseSchema, 400: ErrorResponse},
             tags=["Bogie Checksheets"],
             summary="Create Bogie Checksheet",
             description="Create a new bogie checksheet form with inspection data")
def create_bogie_checksheet(request, payload: BogieChecksheetCreateSchema):
    """
    Create a new bogie checksheet with detailed inspection data.
    
    This endpoint accepts bogie checksheet data including:
    - Form metadata (form number, inspector, date)
    - Bogie details (bogie number, maker, etc.)
    - Bogie condition assessments
    - BMBC component conditions
    """
    try:
        # Get the user object from inspection_by ID
        try:
            user = User.objects.get(id=payload.inspection_by)
        except (User.DoesNotExist, ValueError):
            return 400, {
                "success": False,
                "message": "Invalid user ID provided",
                "errors": {"inspection_by": ["User not found"]}
            }
        
        # Check if form number already exists
        if BogieChecksheet.objects.filter(form_number=payload.form_number).exists():
            return 400, {
                "success": False,
                "message": "Form number already exists",
                "errors": {"form_number": ["This form number is already in use"]}
            }
        
        # Create bogie checksheet
        bogie_checksheet = BogieChecksheet.objects.create(
            form_number=payload.form_number,
            inspection_by=user,
            inspection_date=payload.inspection_date,
            # Bogie details
            bogie_no=payload.bogie_details.bogie_no,
            maker_year_built=payload.bogie_details.maker_year_built,
            incoming_div_and_date=payload.bogie_details.incoming_div_and_date,
            deficit_components=payload.bogie_details.deficit_components,
            date_of_ioh=payload.bogie_details.date_of_ioh,
            # Bogie checksheet conditions
            bogie_frame_condition=payload.bogie_checksheet.bogie_frame_condition,
            bolster=payload.bogie_checksheet.bolster,
            bolster_suspension_bracket=payload.bogie_checksheet.bolster_suspension_bracket,
            lower_spring_seat=payload.bogie_checksheet.lower_spring_seat,
            axle_guide=payload.bogie_checksheet.axle_guide,
            # BMBC checksheet conditions
            cylinder_body=payload.bmbc_checksheet.cylinder_body,
            piston_trunnion=payload.bmbc_checksheet.piston_trunnion,
            adjusting_tube=payload.bmbc_checksheet.adjusting_tube,
            plunger_spring=payload.bmbc_checksheet.plunger_spring,
            status='submitted'
        )
        
        return 201, {
            "success": True,
            "message": "Bogie checksheet submitted successfully.",
            "data": {
                "formNumber": bogie_checksheet.form_number,
                "inspectionBy": str(bogie_checksheet.inspection_by.id),
                "inspectionDate": bogie_checksheet.inspection_date,
                "status": bogie_checksheet.status.title()
            }
        }
        
    except Exception as e:
        return 400, {
            "success": False,
            "message": f"Error creating bogie checksheet: {str(e)}",
            "errors": {"general": [str(e)]}
        }


@router.get("/bogie-checksheets",
            response={200: BogieChecksheetListResponseSchema, 400: ErrorResponse},
            tags=["Bogie Checksheets"],
            summary="Get Bogie Checksheets",
            description="Retrieve bogie checksheets with optional filtering")
def get_bogie_checksheets(
    request,
    form_number: Optional[str] = None,
    inspection_by: Optional[str] = None,
    inspection_date: Optional[date] = None,
    bogie_no: Optional[str] = None
):
    """
    Retrieve bogie checksheets with optional filtering.
    
    Filter parameters:
    - formNumber: Filter by specific form number
    - inspectionBy: Filter by user ID who inspected the form
    - inspectionDate: Filter by inspection date
    - bogieNo: Filter by bogie number
    """
    try:
        # Start with all bogie checksheets
        queryset = BogieChecksheet.objects.all().select_related('inspection_by')
        filters_applied = False
        
        # Apply filters
        if form_number:
            queryset = queryset.filter(form_number__icontains=form_number)
            filters_applied = True
        if inspection_by:
            try:
                user = User.objects.get(id=inspection_by)
                queryset = queryset.filter(inspection_by=user)
                filters_applied = True
            except (User.DoesNotExist, ValueError):
                return 400, {
                    "success": False,
                    "message": "Invalid user ID provided",
                    "errors": {"inspection_by": ["User not found"]}
                }
        if inspection_date:
            queryset = queryset.filter(inspection_date=inspection_date)
            filters_applied = True
        if bogie_no:
            queryset = queryset.filter(bogie_no__icontains=bogie_no)
            filters_applied = True
        
        # Convert to response format
        data = []
        for checksheet in queryset:
            # Create response data dict with proper structure
            response_data = {
                "formNumber": checksheet.form_number,
                "inspectionBy": str(checksheet.inspection_by.id),
                "inspectionDate": checksheet.inspection_date,
                "status": checksheet.status.title(),
                "bogieDetails": {
                    "bogieNo": checksheet.bogie_no,
                    "makerYearBuilt": checksheet.maker_year_built,
                    "incomingDivAndDate": checksheet.incoming_div_and_date,
                    "deficitComponents": checksheet.deficit_components,
                    "dateOfIOH": checksheet.date_of_ioh
                },
                "bogieChecksheet": {
                    "bogieFrameCondition": checksheet.bogie_frame_condition,
                    "bolster": checksheet.bolster,
                    "bolsterSuspensionBracket": checksheet.bolster_suspension_bracket,
                    "lowerSpringSeat": checksheet.lower_spring_seat,
                    "axleGuide": checksheet.axle_guide
                },
                "bmbcChecksheet": {
                    "cylinderBody": checksheet.cylinder_body,
                    "pistonTrunnion": checksheet.piston_trunnion,
                    "adjustingTube": checksheet.adjusting_tube,
                    "plungerSpring": checksheet.plunger_spring
                }
            }
            data.append(response_data)
        
        if filters_applied:
            message = "Filtered bogie checksheet forms fetched successfully."
        else:
            message = "All bogie checksheet forms fetched successfully."
        
        return 200, {
            "success": True,
            "message": message,
            "data": data
        }
        
    except Exception as e:
        return 400, {
            "success": False,
            "message": f"Error retrieving bogie checksheets: {str(e)}",
            "errors": {"general": [str(e)]}
        } 