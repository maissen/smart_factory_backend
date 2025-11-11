from fastapi import APIRouter
from .get_machine_log_route import router as get_log_route
from .create_machine_log_route import router as create_log_route

router = APIRouter()
router.include_router(get_log_route)
router.include_router(create_log_route)