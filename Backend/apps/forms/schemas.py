"""
Pydantic schemas for forms API endpoints.
"""
from typing import Optional, List
from datetime import date
from ninja import Schema
from pydantic import Field


# Base response schemas
class BaseResponse(Schema):
    success: bool
    message: str


class ErrorResponse(Schema):
    success: bool = False
    message: str
    errors: Optional[dict] = None


# Wheel Specification Schemas
class WheelSpecificationFieldsSchema(Schema):
    """Schema for wheel specification measurement fields"""
    tread_diameter_new: str = Field(..., alias="treadDiameterNew", description="e.g., 915 (900-1000)")
    last_shop_issue_size: str = Field(..., alias="lastShopIssueSize", description="e.g., 837 (800-900)")
    condemning_dia: str = Field(..., alias="condemningDia", description="e.g., 825 (800-900)")
    wheel_gauge: str = Field(..., alias="wheelGauge", description="e.g., 1600 (+2,-1)")
    variation_same_axle: str = Field(..., alias="variationSameAxle", description="e.g., 0.5")
    variation_same_bogie: str = Field(..., alias="variationSameBogie", description="e.g., 5")
    variation_same_coach: str = Field(..., alias="variationSameCoach", description="e.g., 13")
    wheel_profile: str = Field(..., alias="wheelProfile", description="e.g., 29.4 Flange Thickness")
    intermediate_wwp: str = Field(..., alias="intermediateWWP", description="e.g., 20 TO 28")
    bearing_seat_diameter: str = Field(..., alias="bearingSeatDiameter", description="e.g., 130.043 TO 130.068")
    roller_bearing_outer_dia: str = Field(..., alias="rollerBearingOuterDia", description="e.g., 280 (+0.0/-0.035)")
    roller_bearing_bore_dia: str = Field(..., alias="rollerBearingBoreDia", description="e.g., 130 (+0.0/-0.025)")
    roller_bearing_width: str = Field(..., alias="rollerBearingWidth", description="e.g., 93 (+0/-0.250)")
    axle_box_housing_bore_dia: str = Field(..., alias="axleBoxHousingBoreDia", description="e.g., 280 (+0.030/+0.052)")
    wheel_disc_width: str = Field(..., alias="wheelDiscWidth", description="e.g., 127 (+4/-0)")

    class Config:
        allow_population_by_field_name = True


class WheelSpecificationCreateSchema(Schema):
    """Schema for creating wheel specifications"""
    form_number: str = Field(..., alias="formNumber", max_length=50)
    submitted_by: str = Field(..., alias="submittedBy")
    submitted_date: date = Field(..., alias="submittedDate")
    fields: WheelSpecificationFieldsSchema


class WheelSpecificationResponseDataSchema(Schema):
    """Schema for wheel specification response data"""
    form_number: str = Field(..., alias="formNumber")
    submitted_by: str = Field(..., alias="submittedBy") 
    submitted_date: date = Field(..., alias="submittedDate")
    status: str
    fields: Optional[WheelSpecificationFieldsSchema] = None


class WheelSpecificationCreateResponseSchema(BaseResponse):
    """Schema for wheel specification creation response"""
    data: WheelSpecificationResponseDataSchema


class WheelSpecificationListResponseSchema(BaseResponse):
    """Schema for wheel specification list response"""
    data: List[WheelSpecificationResponseDataSchema]


# Bogie Checksheet Schemas
class BogieDetailsSchema(Schema):
    """Schema for bogie details section"""
    bogie_no: str = Field(..., alias="bogieNo", max_length=50)
    maker_year_built: str = Field(..., alias="makerYearBuilt", max_length=100)
    incoming_div_and_date: str = Field(..., alias="incomingDivAndDate", max_length=200)
    deficit_components: str = Field(default="None", alias="deficitComponents")
    date_of_ioh: date = Field(..., alias="dateOfIOH")


class BogieChecksheetSchema(Schema):
    """Schema for bogie checksheet section"""
    bogie_frame_condition: str = Field(..., alias="bogieFrameCondition", description="Good, Fair, Poor, or Damaged")
    bolster: str = Field(..., description="Good, Fair, Poor, or Damaged")
    bolster_suspension_bracket: str = Field(..., alias="bolsterSuspensionBracket", description="Good, Fair, Poor, Cracked, or Damaged")
    lower_spring_seat: str = Field(..., alias="lowerSpringSeat", description="Good, Fair, Poor, or Damaged")
    axle_guide: str = Field(..., alias="axleGuide", description="Good, Fair, Worn, or Damaged")


class BMBCChecksheetSchema(Schema):
    """Schema for BMBC checksheet section"""
    cylinder_body: str = Field(..., alias="cylinderBody", description="GOOD, FAIR, WORN OUT, or DAMAGED")
    piston_trunnion: str = Field(..., alias="pistonTrunnion", description="GOOD, FAIR, WORN OUT, or DAMAGED")
    adjusting_tube: str = Field(..., alias="adjustingTube", description="GOOD, FAIR, WORN OUT, or DAMAGED")
    plunger_spring: str = Field(..., alias="plungerSpring", description="GOOD, FAIR, WORN OUT, or DAMAGED")


# Response schemas for bogie checksheet data retrieval
class BogieDetailsResponseSchema(Schema):
    """Schema for bogie details in response"""
    bogie_no: str = Field(..., alias="bogieNo")
    maker_year_built: str = Field(..., alias="makerYearBuilt")
    incoming_div_and_date: str = Field(..., alias="incomingDivAndDate")
    deficit_components: str = Field(..., alias="deficitComponents")
    date_of_ioh: date = Field(..., alias="dateOfIOH")

    class Config:
        allow_population_by_field_name = True


class BogieChecksheetResponseSchema(Schema):
    """Schema for bogie checksheet in response"""
    bogie_frame_condition: str = Field(..., alias="bogieFrameCondition")
    bolster: str
    bolster_suspension_bracket: str = Field(..., alias="bolsterSuspensionBracket")
    lower_spring_seat: str = Field(..., alias="lowerSpringSeat")
    axle_guide: str = Field(..., alias="axleGuide")

    class Config:
        allow_population_by_field_name = True


class BMBCChecksheetResponseSchema(Schema):
    """Schema for BMBC checksheet in response"""
    cylinder_body: str = Field(..., alias="cylinderBody")
    piston_trunnion: str = Field(..., alias="pistonTrunnion")
    adjusting_tube: str = Field(..., alias="adjustingTube")
    plunger_spring: str = Field(..., alias="plungerSpring")

    class Config:
        allow_population_by_field_name = True


class BogieChecksheetCreateSchema(Schema):
    """Schema for creating bogie checksheets"""
    form_number: str = Field(..., alias="formNumber", max_length=50)
    inspection_by: str = Field(..., alias="inspectionBy")
    inspection_date: date = Field(..., alias="inspectionDate")
    bogie_details: BogieDetailsSchema = Field(..., alias="bogieDetails")
    bogie_checksheet: BogieChecksheetSchema = Field(..., alias="bogieChecksheet")
    bmbc_checksheet: BMBCChecksheetSchema = Field(..., alias="bmbcChecksheet")


class BogieChecksheetResponseDataSchema(Schema):
    """Schema for bogie checksheet response data"""
    form_number: str = Field(..., alias="formNumber")
    inspection_by: str = Field(..., alias="inspectionBy")
    inspection_date: date = Field(..., alias="inspectionDate")
    status: str
    bogie_details: Optional[BogieDetailsResponseSchema] = Field(None, alias="bogieDetails")
    bogie_checksheet: Optional[BogieChecksheetResponseSchema] = Field(None, alias="bogieChecksheet")
    bmbc_checksheet: Optional[BMBCChecksheetResponseSchema] = Field(None, alias="bmbcChecksheet")

    class Config:
        allow_population_by_field_name = True


class BogieChecksheetCreateResponseSchema(BaseResponse):
    """Schema for bogie checksheet creation response"""
    data: BogieChecksheetResponseDataSchema


class BogieChecksheetListResponseSchema(BaseResponse):
    """Schema for bogie checksheet list response"""
    data: List[BogieChecksheetResponseDataSchema]


# Filter schemas for GET requests
class WheelSpecificationFilterSchema(Schema):
    """Schema for wheel specification filtering"""
    form_number: Optional[str] = Field(None, alias="formNumber")
    submitted_by: Optional[str] = Field(None, alias="submittedBy")
    submitted_date: Optional[date] = Field(None, alias="submittedDate")


class BogieChecksheetFilterSchema(Schema):
    """Schema for bogie checksheet filtering"""
    form_number: Optional[str] = Field(None, alias="formNumber")
    inspection_by: Optional[str] = Field(None, alias="inspectionBy")
    inspection_date: Optional[date] = Field(None, alias="inspectionDate")
    bogie_no: Optional[str] = Field(None, alias="bogieNo") 