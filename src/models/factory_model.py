from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship

from src.core.db_vars import Base


class Factory(Base):
    __tablename__ = "factories"

    id = Column(Integer, primary_key=True, index=True, comment="Factory ID")
    name = Column(String(150), nullable=False, comment="Factory name")
    location = Column(String(255), nullable=False, comment="Factory location")
    description = Column(Text, nullable=True, comment="Factory description")

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, comment="Factory owner (client)")
    owner = relationship("User", backref="factory", uselist=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    __table_args__ = (
        UniqueConstraint("owner_id", name="unique_owner_factory"),
    )
