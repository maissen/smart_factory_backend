from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.models.machine_model import Machine


def create_machine_crud(
    db: Session,
    factory_id: int,
    name: str,
    serial_number: str,
    status: str = None,
    last_maintenance_date=None,
    description: str = None,
) -> Machine:
    machine = Machine(
        factory_id=factory_id,
        name=name,
        serial_number=serial_number,
        status=status,
        last_maintenance_date=last_maintenance_date,
        description=description,
    )

    db.add(machine)
    db.commit()
    db.refresh(machine)
    return machine


def get_factory_machines_crud(
    db: Session,
    factory_id: int | None = None,
) -> list[Machine]:
    query = db.query(Machine)
    if factory_id is not None:
        query = query.filter(Machine.factory_id == factory_id)
    return query.all()


def update_machine_crud(
    db: Session,
    machine_id: int,
    name: str | None = None,
    serial_number: str | None = None,
    status: str | None = None,
    last_maintenance_date=None,
    description: str | None = None,
) -> Machine:
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise NoResultFound("Machine not found")

    if name is not None:
        machine.name = name
    if serial_number is not None:
        machine.serial_number = serial_number
    if status is not None:
        machine.status = status
    if last_maintenance_date is not None:
        machine.last_maintenance_date = last_maintenance_date
    if description is not None:
        machine.description = description

    db.commit()
    db.refresh(machine)
    return machine


def delete_machine_crud(
    db: Session,
    machine_id: int,
) -> None:
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise NoResultFound("Machine not found")

    db.delete(machine)
    db.commit()
