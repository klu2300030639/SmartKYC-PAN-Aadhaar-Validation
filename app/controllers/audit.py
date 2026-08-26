"""
System Security Audit Logs Controller.
Provides chronological system audit trails and action monitoring.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.schemas import AuditLogItem
from app.controllers.auth import require_admin

router = APIRouter()


@router.get("", response_model=List[AuditLogItem])
def get_audit_logs(
    module: Optional[str] = Query(None, description="Filter by system module"),
    action: Optional[str] = Query(None, description="Filter by action code"),
    limit: int = Query(100, ge=1, le=500),
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Retrieves system audit logs (Admin only)."""
    query = db.query(AuditLog)
    
    if module:
        query = query.filter(AuditLog.module == module)
    if action:
        query = query.filter(AuditLog.action == action)
        
    results = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    
    items = []
    for r in results:
        items.append(
            AuditLogItem(
                log_id=r.log_id,
                action=r.action,
                module=r.module,
                description=r.description,
                created_at=r.created_at,
                performed_by=r.user.username if r.user else "System"
            )
        )
    return items

