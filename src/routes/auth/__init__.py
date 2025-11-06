from fastapi import APIRouter
from .login_route import router as login_router

router = APIRouter()
router.include_router(login_router)
