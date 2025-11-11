from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.models.machine_model import Machine


def create_machine_crud(
    db: Session,
    factory_id: int,
    name: str,
    serial_number: str,
    last_maintenance_date=None,
    description: str = None,
) -> Machine:
    machine = Machine(
        factory_id=factory_id,
        name=name,
        serial_number=serial_number,
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
    last_maintenance_date=None,
    description: str | None = None,
) -> Machine:
    machine = db.query(Machine).filter(Machine.id == machine_id).first()

    if name is not None:
        machine.name = name
    if serial_number is not None:
        machine.serial_number = serial_number
    if last_maintenance_date is not None:
        machine.last_maintenance_date = last_maintenance_date
    if description is not None:
        machine.description = description

    db.commit()
    db.refresh(machine)
    return machine


def update_machine_status_crud(
    db: Session,
    machine_id: int,
    status: str,
) -> Machine:
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    machine.status = status

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


def get_machine_by_serial_crud(db: Session, serial_number: str) -> Machine | None:
    """
    Retrieve a machine by its serial number.

    Returns None if not found.
    """
    return db.query(Machine).filter(Machine.serial_number == serial_number).first()


def get_machine_by_name_crud(db: Session, name: str) -> Machine | None:
    """
    Retrieve a machine by its name.

    Returns None if not found.
    """
    return db.query(Machine).filter(Machine.name == name).first()


def get_machine_by_id_crud(db: Session, machine_id: int):
    """
    Retrieve a machine by its ID.
    
    Returns None if not found.
    """
    return db.query(Machine).filter(Machine.id == machine_id).first()


def load_all_machines_crud(db: Session) -> list[Machine]:
    return db.query(Machine).all()
