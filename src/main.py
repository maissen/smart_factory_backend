from fastapi import FastAPI, Depends
from src.dependencies.get_current_user_dependency import get_current_user
from src.schema.user_schema import UserResponse
from src.core.settings import settings
from src.routes.user.create_user_route import router as register_route
from src.routes.auth.login_route import router as login_route
from src.routes.user.get_all_users_route import router as get_users_route
from src.schema.user_schema import UserResponse

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(register_route, prefix="/api/users")
app.include_router(get_users_route, prefix="/api/users")
app.include_router(login_route, prefix="/api/login")

@app.on_event("startup")
def startup_event():
    print(f"{settings.PROJECT_NAME} started successfully!")


@app.get("/me", response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Get info about the currently logged-in user.
    """
    return current_user
