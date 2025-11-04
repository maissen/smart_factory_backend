# SmartFactory Portal

SmartFactory Portal is a comprehensive digital platform designed to streamline factory operations management. It provides factory owners and operators with real-time visibility into machine performance, maintenance schedules, and operational metrics through an intuitive web interface.

---

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.9+ (for local development)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Configure database credentials and application settings

3. **Docker Deployment**
   ```bash
   docker-compose up -d
   ```

4. **Access the Application**
   - API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

---

## Architecture

```
backend/
├── alembic/                    # Database migration management
├── alembic.ini                 # Alembic configuration
├── api_contracts/              # API specifications and contracts
├── docker-compose.yml          # Container orchestration
├── Dockerfile                  # Container image definition
├── requirements.txt            # Python dependencies
│
└── src/
    ├── main.py                 # Application entry point
    ├── core/
    │   ├── postgres_config.py  # PostgreSQL database configuration
    │   └── settings.py         # Application settings and environment config
    │
    └── models/
        └── user_model.py       # User data model definition
```

### Architecture Overview

**Technology Stack:**
- **Framework**: FastAPI (Python web framework for building APIs)
- **Database**: PostgreSQL (relational database for data persistence)
- **Migration Tool**: Alembic (database schema version control)
- **Containerization**: Docker & Docker Compose (for consistent deployment)

**Core Components:**

1. **Application Core** (`src/core/`)
   - `settings.py`: Centralizes application configuration, environment variables, and global settings
   - `postgres_config.py`: Handles database connection setup, connection pooling, and PostgreSQL-specific configurations

2. **Data Models** (`src/models/`)
   - `user_model.py`: Defines the user entity structure including authentication and authorization attributes
   - Built with SQLAlchemy ORM for database abstraction

3. **Database Migrations** (`alembic/`)
   - Version-controlled schema changes
   - Ensures consistent database state across environments

4. **API Contracts** (`api_contracts/`)
   - Request/response schemas and validation rules

5. **Application Entry** (`src/main.py`)
   - FastAPI application initialization

---

## Development Workflow

### Adding New Database Models

The project uses Alembic for database migrations with automatic model detection. Follow these steps to add a new model:

1. **Create your model file**

2. **Register the model in Alembic**
   
   Edit `alembic/env.py` and import your new model:
   ```python
   # alembic/env.py
   # Import all models here so Alembic can detect them
   from src.models.user_model import User
   from src.models.new_model import My_model  # Add your new model
   ```

3. **Generate migration**
   
   Access the backend container:
   ```bash
   docker exec -it backend_api sh
   ```
   
   Create an auto-generated migration:
   ```bash
   alembic revision --autogenerate -m "Create machine model"
   ```

4. **Review and apply migration**
   
   Check the generated migration file in `alembic/versions/`, then apply it:
   ```bash
   alembic upgrade head
   ```

5. **Exit container**
   ```bash
   exit
   ```

**Important Notes:**
- Always import new models in `alembic/env.py` for Alembic to detect schema changes
- Review auto-generated migrations before applying them
- Use descriptive migration messages
- Test migrations in development before production deployment

---



## 🤝 Contributing

Contributions are welcome! Please follow the standard Git workflow:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
