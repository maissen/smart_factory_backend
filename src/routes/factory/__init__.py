from fastapi import APIRouter
from .create_factory_route import router as create_route
from .get_factory_route import router as get_factory_route

router = APIRouter()
router.include_router(create_route)
router.include_router(get_factory_route)
