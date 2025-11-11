from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship, backref
from src.core.db_vars import Base

class MachineLog(Base): 
    __tablename__ = "machine_logs"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(
        Integer,
        ForeignKey("machines.id", ondelete="CASCADE"),
        nullable=False,
    )

    machine = relationship(
        "Machine",
        backref=backref("logs", passive_deletes=True)
    )

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("status IN ('Running', 'Idle', 'Maintenance', 'Stopped')"),
    )
