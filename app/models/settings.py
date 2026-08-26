"""
Application Settings Model.
Stores key-value configuration flags.
"""
from sqlalchemy import Column, Integer, String
from app.database import Base


class ApplicationSetting(Base):
    __tablename__ = "application_settings"

    setting_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    setting_key = Column(String(50), unique=True, nullable=False)
    setting_value = Column(String(255), nullable=False)
