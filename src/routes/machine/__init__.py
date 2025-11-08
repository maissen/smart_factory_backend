from fastapi import APIRouter
from .get_machines_of_factory_route import router as get_machines_route
from .create_machine_route import router as create_machine_route


router = APIRouter()
router.include_router(get_machines_route)
router.include_router(create_machine_route)