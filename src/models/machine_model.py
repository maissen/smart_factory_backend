from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    func,
    CheckConstraint,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from src.core.db_vars import Base
from src.core.settings import settings


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True, comment="Machine ID")

    factory_id = Column(Integer, ForeignKey("factories.id", ondelete="CASCADE"), nullable=False, comment="Linked factory")
    factory = relationship("Factory", backref="machines")

    name = Column(String(150), nullable=False, unique=True, comment="Unique machine name")
    serial_number = Column(String(100), nullable=False, unique=True, comment="Unique serial number")

    status = Column(
        String(20),
        nullable=False,
        server_default="Idle",
        comment="Machine status"
    )

    last_maintenance_date = Column(Date, nullable=True, comment="Last maintenance date")
    description = Column(Text, nullable=True, comment="Notes or details")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    __table_args__ = (
        CheckConstraint(
            f"status IN ('Running', 'Idle', 'Maintenance', 'Stopped')",
            name="valid_machine_status"
        ),
        UniqueConstraint("name", name="unique_machine_name"),
        UniqueConstraint("serial_number", name="unique_machine_serial"),
    )
