from fastapi import APIRouter
from .create_user_route import router as create_user
from .get_all_users_route import router as get_users
from .delete_user_route import router as delete_user
from .update_user_route import router as update_user
from .update_user_password_route import router as update_password

router = APIRouter()
router.include_router(create_user)
router.include_router(get_users)
router.include_router(delete_user)
router.include_router(update_user)
router.include_router(update_password)
