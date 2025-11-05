from sqlalchemy.orm import Session
from src.db_crud.users.update_user_crud import update_user_crud
from src.helpers.str_helpers import validate_email, validate_phone_number


def update_user_service(
    db: Session,
    user_id: int,
    full_name: str,
    email: str,
    phone_number: str,
    role: str
):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("User ID must be a positive integer")

    if not full_name or not isinstance(full_name, str):
        raise ValueError("Full name is required")

    validated_email = validate_email(email)
    validated_phone = validate_phone_number(phone_number)

    try:
        updated_user = update_user_crud(
            db=db,
            user_id=user_id,
            full_name=full_name,
            email=validated_email,
            phone_number=validated_phone,
            role=role,
        )

    except ValueError as e:
        raise ValueError(e)

    except Exception as e:
        raise RuntimeError(f"Failed to update user: {e}")

    return updated_user
