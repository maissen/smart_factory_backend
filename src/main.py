from fastapi import FastAPI
from src.core.settings import settings
from src.routes.user.create_user_route import router as register_route

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(register_route, prefix="/api/users")

@app.on_event("startup")
def startup_event():
    print(f"{settings.PROJECT_NAME} started successfully!")
