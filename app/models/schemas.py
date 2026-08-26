"""
Pydantic Validation Schemas for REST API endpoints.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# --- Auth Schemas ---
class LoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    full_name: str
    username: str
    email: str
    phone: Optional[str] = None
    role: str
    status: str
    created_at: datetime


class UserCreateRequest(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    phone: Optional[str] = None
    role: str = "User"


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    password: Optional[str] = None


# --- Validation Schemas ---
class PANValidateRequest(BaseModel):
    pan_number: str = Field(...)


class AadhaarValidateRequest(BaseModel):
    aadhaar_number: str = Field(...)


class ValidationResultResponse(BaseModel):
    valid: bool
    document_type: str
    document_number: str
    reason: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime


class ValidationHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    validation_id: int
    document_type: str
    document_number: str
    status: str
    reason: Optional[str] = None
    validated_at: datetime
    validated_by: Optional[str] = None



# --- Dashboard KPI Schemas ---
class DashboardStats(BaseModel):
    total_validations: int
    valid_count: int
    invalid_count: int
    success_rate: float
    pan_count: int
    aadhaar_count: int
    recent_validations: List[ValidationHistoryItem]


# --- Audit Schemas ---
class AuditLogItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    log_id: int
    action: str
    module: str
    description: Optional[str] = None
    created_at: datetime
    performed_by: Optional[str] = None


