from sqlalchemy.orm import Session
from src.db_crud.users.get_user_crud import get_all_users_crud


def get_all_users_service(db: Session, role: str | None = None):
    """
    Service function to retrieve all users, optionally filtered by role.
    Includes validation and controlled exception behavior.
    """

    # Validate role
    if role is not None:
        if not isinstance(role, str):
            raise ValueError("Role must be a string")
        
        if role.strip() == "":
            raise ValueError("Role cannot be an empty string")

    try:
        users = get_all_users_crud(db, role)

    except Exception as exc:
        # Something went wrong with the DB
        raise RuntimeError(f"Failed to fetch users: {exc}")

    return users
