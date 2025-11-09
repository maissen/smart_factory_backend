import docker
from src.exceptions.machine_exceptions import MachineError
from src.helpers.machine import validate_machine_id

def launch_vm_container(machine_id: int):

    validate_machine_id(machine_id)
    
    try:
        # Start VM container
        client = docker.from_env()
        client.containers.run(
            image="smartfactory_vm",
            name=f"vm_{machine_id}",
            environment={
                "MACHINE_ID": str(machine_id),
                "METRICS_ENDPOINT": f"http://backend_api:8000/api/metrics/insert"
            },
            network="smart_factory_network",
            detach=True,
            restart_policy={"Name": "always"}
        )
    
    except Exception as e:
        print(e)
        raise MachineError("Failed to create a virtual version of your machine.")

