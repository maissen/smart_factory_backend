### Adding New Database Models to Postgres

The project uses Alembic for database migrations with automatic model detection. Follow these steps to add a new model:

1. **Create your model file** in models/your_model.py

2. **Register the model in Alembic**
   
   Edit `alembic/env.py` and import your new model:
   ```python
   # alembic/env.py
   # Import all models here so Alembic can detect them
   from src.models.user_model import User
   from src.models.your_model import New_model  # Add your new model
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