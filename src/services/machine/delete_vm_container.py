import docker
from src.helpers.machine import validate_machine_id
from src.exceptions.machine_exceptions import MachineError

def delete_vm_container(machine_id):
    validate_machine_id(machine_id)
    client = docker.from_env()

    try:
        container = client.containers.get(f"vm_{machine_id}")

        # Force kill immediately (SIGKILL equivalent)
        container.kill()

        # Force remove even if it's still in weird state
        container.remove(force=True)

    except Exception as e:
        print(e)
        raise MachineError("Failed to force kill and remove your machine container.")
