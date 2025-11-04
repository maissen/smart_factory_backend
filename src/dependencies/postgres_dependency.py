# Dependency for FastAPI routes
from src.core.db_vars import SessionLocal


def get_db():
    """Provide a synchronous DB session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
