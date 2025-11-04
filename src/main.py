from fastapi import FastAPI
from src.core.settings import settings

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print(f"{settings.PROJECT_NAME} started successfully!")
