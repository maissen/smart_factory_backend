from sqlalchemy import Column, Integer, String, Time, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from src.core.db_vars import Base


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True, comment="Shift ID")

    factory_id = Column(
        Integer,
        ForeignKey("factories.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        comment="One shift per factory"
    )
    factory = relationship("Factory", backref="shift", uselist=False)

    name = Column(String(100), nullable=False, comment="Shift name")
    start_time = Column(Time, nullable=False, comment="Shift start time")
    end_time = Column(Time, nullable=False, comment="Shift end time")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Created timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Updated timestamp")

    __table_args__ = (
        UniqueConstraint("factory_id", name="unique_factory_shift"),
    )
