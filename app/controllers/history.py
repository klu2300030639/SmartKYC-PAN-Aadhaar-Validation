"""
KYC Validation History Controller.
Provides historical records, search/filtering, and CSV export.
"""
import io
import csv
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.validation import ValidationHistory
from app.models.schemas import ValidationHistoryItem
from app.controllers.auth import require_auth, require_admin

router = APIRouter()


@router.get("", response_model=List[ValidationHistoryItem])
def get_history(
    doc_type: Optional[str] = Query(None, description="Filter by 'PAN' or 'Aadhaar'"),
    status: Optional[str] = Query(None, description="Filter by 'VALID' or 'INVALID'"),
    search: Optional[str] = Query(None, description="Search document number"),
    limit: int = Query(100, ge=1, le=500),
    user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Retrieves filtered validation history records."""
    query = db.query(ValidationHistory)
    
    if user.role != "Admin":
        query = query.filter(ValidationHistory.user_id == user.user_id)
        
    if doc_type:
        query = query.filter(ValidationHistory.document_type == doc_type)
        
    if status:
        query = query.filter(ValidationHistory.status == status)
        
    if search:
        query = query.filter(ValidationHistory.document_number.like(f"%{search.strip()}%"))
        
    results = query.order_by(ValidationHistory.validated_at.desc()).limit(limit).all()
    
    items = []
    for r in results:
        items.append(
            ValidationHistoryItem(
                validation_id=r.validation_id,
                document_type=r.document_type,
                document_number=r.document_number,
                status=r.status,
                reason=r.reason,
                validated_at=r.validated_at,
                validated_by=r.user.username if r.user else "System"
            )
        )
    return items


@router.get("/export")
def export_history_csv(
    user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Exports all validation records as a downloadable CSV file (Admins only)."""
    results = db.query(ValidationHistory).order_by(ValidationHistory.validated_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Document Type", "Document Number", "Status", "Reason / Details", "Validated At", "Validated By"])
    
    for r in results:
        writer.writerow([
            r.validation_id,
            r.document_type,
            r.document_number,
            r.status,
            r.reason or "N/A",
            r.validated_at.strftime("%Y-%m-%d %H:%M:%S"),
            r.user.username if r.user else "System"
        ])

        
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=SmartKYC_Validation_History.csv"}
    )
