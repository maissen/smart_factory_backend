from sqlalchemy.orm import Session
from src.db_crud.users.create_user import create_user_crud
from src.helpers.str_helpers import validate_email, validate_password, validate_phone_number, is_valid_str, normalize_str
from src.services.user import get_user_by_email_service, get_user_by_phone_number_service


def create_user_service(
    db: Session,
    full_name: str,
    email: str,
    password: str,
    role: str,
    phone_number: str
):
    """
    Service function that validates inputs and calls CRUD layer.
    """

    if is_valid_str(value=full_name):
        raise ValueError("Full name is required")
    
    full_name = normalize_str(full_name)
    

    validated_email = validate_email(email)
    validated_password = validate_password(password)
    validated_phone = validate_phone_number(phone_number)

    # check if credentials exist or not
    get_user_by_email_service(db=db, email=email)
    get_user_by_phone_number_service(db=db, phone_number=phone_number)

    try:
        new_user = create_user_crud(
            db=db,
            full_name=full_name,
            email=validated_email,
            password=validated_password,
            role=role,
            phone_number=validated_phone
        )

    except ValueError as e:
        # duplicate email/phone or invalid role
        raise ValueError(e)
    
    except Exception as e:
        raise RuntimeError(f"Failed to create user: {e}")

    return new_user
