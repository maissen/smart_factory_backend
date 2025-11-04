from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print(f"app started successfully!")
