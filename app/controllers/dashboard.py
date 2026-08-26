"""
Dashboard Controller.
Aggregates key performance metrics, success ratios, and analytics.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.validation import ValidationHistory
from app.models.schemas import DashboardStats, ValidationHistoryItem
from app.controllers.auth import require_auth

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(user: User = Depends(require_auth), db: Session = Depends(get_db)):
    """Computes real-time KPIs and chart metrics for the dashboard."""
    query = db.query(ValidationHistory)
    if user.role != "Admin":
        query = query.filter(ValidationHistory.user_id == user.user_id)
        
    total_count = query.count()
    valid_count = query.filter(ValidationHistory.status == "VALID").count()
    invalid_count = query.filter(ValidationHistory.status == "INVALID").count()
    
    pan_count = query.filter(ValidationHistory.document_type == "PAN").count()
    aadhaar_count = query.filter(ValidationHistory.document_type == "Aadhaar").count()
    
    success_rate = round((valid_count / total_count * 100.0), 1) if total_count > 0 else 0.0
    
    # Recent 10 validations
    recent_query = query.order_by(ValidationHistory.validated_at.desc()).limit(10).all()
    
    recent_items = []
    for r in recent_query:
        val_by = r.user.username if r.user else "System"
        recent_items.append(
            ValidationHistoryItem(
                validation_id=r.validation_id,
                document_type=r.document_type,
                document_number=r.document_number,
                status=r.status,
                reason=r.reason,
                validated_at=r.validated_at,
                validated_by=val_by
            )
        )

        
    return DashboardStats(
        total_validations=total_count,
        valid_count=valid_count,
        invalid_count=invalid_count,
        success_rate=success_rate,
        pan_count=pan_count,
        aadhaar_count=aadhaar_count,
        recent_validations=recent_items
    )
