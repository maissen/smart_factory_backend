from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint, func
from src.core.postgres_config import Base
from src.core.settings import settings

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="Unique user ID")
    Full_name = Column(String(100), unique=False, nullable=False, comment="User full name")
    email = Column(String(255), unique=True, nullable=False, index=True, comment="User email")

    password_hash = Column(Text, nullable=False, comment="Hashed password")
    role = Column(String(10), nullable=False, comment="Role type: 'admin' or 'client'")
    phone_number = Column(String(20), unique=True, nullable=False, index=True, comment="must be unique if provided")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="When account was created")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update time")

    __table_args__ = (CheckConstraint(role.in_(settings.USER_ALLOWED_ROLES), name="check_role"),)
