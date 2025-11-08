from fastapi import FastAPI
from src.core.settings import settings
from src.routes.user import router as user_routes
from src.routes.auth import router as auth_routes
from src.routes.factory import router as factory_routes
from src.routes.shift import router as shift_routes
from src.routes.machine import router as machine_routes

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(user_routes, prefix="/api/users")
app.include_router(auth_routes, prefix="/api/auth")
app.include_router(factory_routes, prefix="/api/factory")
app.include_router(shift_routes, prefix="/api/shift")
app.include_router(machine_routes, prefix="/api/machine")

@app.on_event("startup")
def startup_event():
    print(f"{settings.PROJECT_NAME} started successfully!")
