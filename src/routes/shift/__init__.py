from fastapi import APIRouter
from .create_shift_route import router as create_route

router = APIRouter()
router.include_router(create_route)