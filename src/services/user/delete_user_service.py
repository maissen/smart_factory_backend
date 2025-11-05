from sqlalchemy.orm import Session
from src.db_crud.users.delete_user import delete_user_crud


def delete_user_by_id_service(db: Session, user_id: int) -> None:
    """
    Service function responsible for validating input
    and delegating deletion to the CRUD layer.
    """

    # Validate user_id
    if not isinstance(user_id, int):
        raise ValueError("User ID must be an integer")

    if user_id <= 0:
        raise ValueError("User ID must be a positive integer")

    try:
        delete_user_crud(db, user_id)

    except ValueError as e:
        # Means user was not found
        raise LookupError(e)
    
    except Exception as e:
        # Any unexpected DB issues
        raise RuntimeError(f"Failed to delete user: {e}")
