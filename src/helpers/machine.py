from src.exceptions.machine_exceptions import MachineError

def validate_machine_id(machine_id: int):
    if not isinstance(machine_id, int) or machine_id <= 0:
        raise MachineError("Machine id is invalid.")