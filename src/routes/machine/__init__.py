from fastapi import APIRouter
from .get_machines_of_factory_route import router as get_machines_route


router = APIRouter()
router.include_router(get_machines_route)