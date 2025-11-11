from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship
from src.core.db_vars import Base

class MachineLog(Base): 
    __tablename__ = "machine_logs"

    id = Column(Integer, primary_key=True, index=True, comment="Log ID")
    
    machine_id = Column(
        Integer,
        ForeignKey("machines.id", ondelete="CASCADE"),
        nullable=False,
        comment="Machine reference"
    )
    machine = relationship("Machine", backref="logs")

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Log timestamp"
    )

    status = Column(
        String(20),
        nullable=True,
        comment="Machine state",
    )

    notes = Column(
        Text,
        nullable=True,
        comment="Comments or system-generated remarks"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('Running', 'Idle', 'Maintenance', 'Fault')",
            name="valid_log_status"
        ),
    )
