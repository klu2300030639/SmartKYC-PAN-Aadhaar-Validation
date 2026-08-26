"""
User Administration Controller.
Manages system accounts, roles (Admin/User/Guest), status, and Danger Zone deletions.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.schemas import UserResponse, UserCreateRequest, UserUpdateRequest
from app.controllers.auth import require_admin
from app.services.security import hash_password

router = APIRouter()


@router.get("", response_model=List[UserResponse])
def list_users(current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Lists all registered users in the directory (Admin only)."""
    return db.query(User).order_by(User.created_at.asc()).all()


@router.post("", response_model=UserResponse)
def create_user(
    payload: UserCreateRequest,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Creates a new user account (Admin only)."""
    existing_username = db.query(User).filter(User.username == payload.username.strip()).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken."
        )
        
    existing_email = db.query(User).filter(User.email == payload.email.strip()).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already registered."
        )
        
    new_user = User(
        full_name=payload.full_name.strip(),
        username=payload.username.strip(),
        email=payload.email.strip(),
        password_hash=hash_password(payload.password),
        phone=payload.phone.strip() if payload.phone else None,
        role=payload.role,
        status="Active"
    )
    db.add(new_user)
    
    audit = AuditLog(
        user_id=current_admin.user_id,
        action="CREATE_USER",
        module="User Directory",
        description=f"Admin {current_admin.username} created user account: {new_user.username} ({new_user.role})"
    )
    db.add(audit)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Updates user roles, status, or passwords (Admin only)."""
    target = db.query(User).filter(User.user_id == user_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        
    if payload.full_name:
        target.full_name = payload.full_name.strip()
    if payload.phone:
        target.phone = payload.phone.strip()
    if payload.role:
        target.role = payload.role
    if payload.status:
        target.status = payload.status
    if payload.password:
        target.password_hash = hash_password(payload.password)
        
    audit = AuditLog(
        user_id=current_admin.user_id,
        action="UPDATE_USER",
        module="User Directory",
        description=f"Admin {current_admin.username} updated account details for {target.username}."
    )
    db.add(audit)
    db.commit()
    db.refresh(target)
    return target


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Permanently deletes a user account with self-deletion protection (Admin only)."""
    target = db.query(User).filter(User.user_id == user_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        
    if target.user_id == current_admin.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Security Protection: You cannot delete your own active administrator account."
        )
        
    deleted_username = target.username
    db.delete(target)
    
    audit = AuditLog(
        user_id=current_admin.user_id,
        action="DELETE_USER",
        module="User Directory",
        description=f"Admin {current_admin.username} permanently deleted user account: {deleted_username}"
    )
    db.add(audit)
    db.commit()
    return {"message": f"User '{deleted_username}' deleted successfully."}
