"""
Authentication Controller.
Handles user login, session management, and RBAC authorization guards.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.schemas import LoginRequest, UserResponse
from app.services.security import verify_password, generate_session_token

router = APIRouter()

# In-memory session store (or cache) mapping token -> user_id
ACTIVE_SESSIONS = {}


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """Dependency: Extracts and verifies current user from session cookie or header."""
    token = request.cookies.get("smartkyc_session") or request.headers.get("X-Session-Token")
    if not token or token not in ACTIVE_SESSIONS:
        return None
    user_id = ACTIVE_SESSIONS[token]
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or user.status != "Active":
        return None
    return user


def require_auth(user: Optional[User] = Depends(get_current_user)) -> User:
    """Guard: Requires authenticated active user."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in."
        )
    return user


def require_admin(user: User = Depends(require_auth)) -> User:
    """Guard: Requires user with Admin role."""
    if user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required to access this resource."
        )
    return user


@router.post("/login", response_model=UserResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """Authenticates username and password, returns UserResponse and sets cookie."""
    user = db.query(User).filter(User.username == payload.username.strip()).first()
    
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )
        
    if user.status != "Active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is currently {user.status}. Please contact administrator."
        )
        
    # Generate session token
    token = generate_session_token()
    ACTIVE_SESSIONS[token] = user.user_id
    
    # Set HTTP-only session cookie
    response.set_cookie(
        key="smartkyc_session",
        value=token,
        httponly=True,
        max_age=86400,  # 24 hours
        samesite="lax"
    )
    
    # Audit log
    audit = AuditLog(
        user_id=user.user_id,
        action="USER_LOGIN",
        module="Authentication",
        description=f"User {user.username} logged in successfully."
    )
    db.add(audit)
    db.commit()
    
    return user


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(require_auth)):
    """Returns profile details of the currently authenticated user."""
    return user


@router.post("/logout")
def logout(request: Request, response: Response, user: Optional[User] = Depends(get_current_user), db: Session = Depends(get_db)):
    """Clears user session and logs the logout event."""
    token = request.cookies.get("smartkyc_session") or request.headers.get("X-Session-Token")
    if token and token in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[token]
        
    response.delete_cookie("smartkyc_session")
    
    if user:
        audit = AuditLog(
            user_id=user.user_id,
            action="USER_LOGOUT",
            module="Authentication",
            description=f"User {user.username} logged out."
        )
        db.add(audit)
        db.commit()
        
    return {"message": "Logged out successfully."}
