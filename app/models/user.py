"""
User Model.
Represents system users, roles (Admin, User, Guest), and account status.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(String(20), default="User", nullable=False)  # 'Admin', 'User', 'Guest'
    status = Column(String(20), default="Active", nullable=False)  # 'Active', 'Suspended', 'Locked'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    validations = relationship("ValidationHistory", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
