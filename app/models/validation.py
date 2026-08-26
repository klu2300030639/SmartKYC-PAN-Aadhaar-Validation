"""
Validation History Model.
Tracks validation requests for PAN and Aadhaar identity documents.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class ValidationHistory(Base):
    __tablename__ = "validation_history"

    validation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    document_type = Column(String(20), nullable=False)  # 'PAN', 'Aadhaar'
    document_number = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False, index=True)  # 'VALID', 'INVALID'
    reason = Column(String(255), nullable=True)
    validated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="validations")

