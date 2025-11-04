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
   - Rename `.env.example` to `.env`

3. **Configure settings** in .env file

4. **Docker Deployment**
   ```bash
   docker-compose up -d
   ```

5. **Access the Application**
   - API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

---

## Architecture
```
backend/
├── alembic/   # Database migrations
│
├── docs/   # Documentation
├── src/
│   ├── main.py       # App entry point
│   ├── core/         # Config & settings
│   └── models/       # Database models
│
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

**Documentation:**
- Click [Architecture](docs/ARCHITECTURE.md) for Detailed project structure
- Click [Database](docs/DATABASE.md) to learn How to add new tables & models to Postgres
- Click [APIs](docs/api_contracts/) to learn How to use API endpoints

### Architecture Overview

**Technology Stack:**
- **Framework**: FastAPI (Python web framework for building APIs)
- **Database**: PostgreSQL (relational database for data persistence)
- **Migration Tool**: Alembic (database schema version control)
- **Containerization**: Docker & Docker Compose (for consistent deployment)

---

## 🤝 Contributing

Contributions are welcome! Please follow the standard Git workflow:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
