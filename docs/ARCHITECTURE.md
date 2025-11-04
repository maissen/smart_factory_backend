## Project Structure

Backend application organized with FastAPI, PostgreSQL, and Docker containerization.
```
backend/
│
├── alembic/                    # Database migration management
├── alembic.ini                 # Alembic configuration
├── api_contracts/              # API specifications and contracts
│
├── docker-compose.yml          # Container orchestration
├── Dockerfile                  # Container image definition
├── requirements.txt            # Python dependencies
│
└── src/
    ├── main.py                 # Application entry point
    │
    ├── core/
    │   ├── postgres_config.py  # PostgreSQL database configuration
    │   └── settings.py         # Application settings and environment config
    │
    └── models/
        └── user_model.py       # User data model definition
```