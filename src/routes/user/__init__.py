from fastapi import APIRouter
from .create_user_route import router as create_user_route
from .get_all_users_route import router as get_users_route
from .delete_user_route import router as delete_user_route
from .update_user_password_route import router as update_password_route
from .update_user_route import router as update_user_route

router = APIRouter()
router.include_router(create_user_route)
router.include_router(get_users_route)
router.include_router(delete_user_route)
router.include_router(update_password_route)
router.include_router(update_user_route)
