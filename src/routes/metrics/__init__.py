from fastapi import APIRouter
from .insert_metrics import router as insert_router


router = APIRouter()
router.include_router(insert_router)