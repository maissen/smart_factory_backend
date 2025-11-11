from fastapi import APIRouter
from .get_machine_log_route import router as get_machine_log_route

router = APIRouter()
router.include_router(get_machine_log_route)