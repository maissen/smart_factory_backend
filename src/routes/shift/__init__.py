from fastapi import APIRouter
from .create_shift_route import router as create_route
from .get_shift_of_factory import router as get_shift_route
from .update_shift_route import router as update_shift_route

router = APIRouter()
router.include_router(create_route)
router.include_router(get_shift_route)
router.include_router(update_shift_route)