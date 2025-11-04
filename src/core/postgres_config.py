from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.settings import settings

# Synchronous engine
# Replace asyncpg with psycopg2 for sync access
engine = create_engine(settings.POSTGRES_DB_URL, echo=True)

# Synchronous session maker
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    """Provide a synchronous DB session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
