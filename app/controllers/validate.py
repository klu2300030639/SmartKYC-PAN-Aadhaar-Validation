"""
Document Validation Controller.
Handles offline algorithmic validations for PAN cards and Aadhaar (Verhoeff) cards.
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.validation import ValidationHistory
from app.models.audit_log import AuditLog
from app.models.schemas import PANValidateRequest, AadhaarValidateRequest, ValidationResultResponse
from app.controllers.auth import require_auth
from app.services.pan_validator import validate_pan
from app.services.verhoeff import validate_aadhaar

router = APIRouter()


@router.post("/pan", response_model=ValidationResultResponse)
def validate_pan_endpoint(
    payload: PANValidateRequest,
    user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Validates a Permanent Account Number (PAN) according to Income Tax rules.
    Records the validation attempt in history and system audit trail.
    """
    res = validate_pan(payload.pan_number)
    status_str = "VALID" if res["valid"] else "INVALID"
    clean_pan = res.get("pan", payload.pan_number.strip().upper())
    
    # Record history
    history = ValidationHistory(
        user_id=user.user_id,
        document_type="PAN",
        document_number=clean_pan,
        status=status_str,
        reason=res["reason"]
    )
    db.add(history)
    
    # Audit log
    audit = AuditLog(
        user_id=user.user_id,
        action="VALIDATE_PAN",
        module="Verification",
        description=f"PAN validation for {clean_pan}: {status_str}"
    )
    db.add(audit)
    db.commit()
    
    return {
        "valid": res["valid"],
        "document_type": "PAN",
        "document_number": clean_pan,
        "reason": res["reason"],
        "details": {
            "entity_type": res.get("entity_type"),
            "entity_code": res.get("entity_code"),
            "surname_initial": res.get("surname_initial")
        } if res["valid"] else None,
        "timestamp": datetime.utcnow()
    }


@router.post("/aadhaar", response_model=ValidationResultResponse)
def validate_aadhaar_endpoint(
    payload: AadhaarValidateRequest,
    user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Validates a 12-digit Aadhaar UID number using the Verhoeff algorithm.
    Records the validation attempt in history and system audit trail.
    """
    res = validate_aadhaar(payload.aadhaar_number)
    status_str = "VALID" if res["valid"] else "INVALID"
    doc_num = res.get("formatted", payload.aadhaar_number.strip())
    
    # Record history
    history = ValidationHistory(
        user_id=user.user_id,
        document_type="Aadhaar",
        document_number=doc_num,
        status=status_str,
        reason=res["reason"]
    )
    db.add(history)
    
    # Audit log
    audit = AuditLog(
        user_id=user.user_id,
        action="VALIDATE_AADHAAR",
        module="Verification",
        description=f"Aadhaar validation for {doc_num}: {status_str}"
    )
    db.add(audit)
    db.commit()
    
    return {
        "valid": res["valid"],
        "document_type": "Aadhaar",
        "document_number": doc_num,
        "reason": res["reason"],
        "details": {
            "formatted": res.get("formatted"),
            "raw": res.get("raw"),
            "algorithm": "Verhoeff Dihedral Group D5"
        } if res["valid"] else None,
        "timestamp": datetime.utcnow()
    }
