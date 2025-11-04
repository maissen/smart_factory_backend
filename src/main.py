from fastapi import FastAPI
from src.core.settings import settings
from src.schema.user_schema import UserCreate

app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
def startup_event():
    print(f"{settings.PROJECT_NAME} started successfully!")

