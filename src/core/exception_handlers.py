from fastapi import Request, status
from fastapi.responses import JSONResponse

# Import all domain exceptions
from src.exceptions.factory_exceptions import *
from src.exceptions.machine_exceptions import *
from src.exceptions.shifts_exceptions import *
from src.exceptions.user_exceptions import *


def register_exception_handlers(app):
    """
    Registers global exception handlers for all domain errors.
    """

    # A mapping of domain exceptions to HTTP status codes.
    # You can extend this anytime without touching routes or services.
    exception_to_status = {

        # ========== FACTORY ==========
        FactoryNotFoundError: status.HTTP_404_NOT_FOUND,
        FactoryOwnerNotFoundError: status.HTTP_404_NOT_FOUND,
        FactoryAlreadyExistsError: status.HTTP_409_CONFLICT,
        FactoryUpdateError: status.HTTP_400_BAD_REQUEST,
        FactoryDeleteError: status.HTTP_400_BAD_REQUEST,
        FactoryPermissionError: status.HTTP_403_FORBIDDEN,
        InvalidFactoryIdError: status.HTTP_400_BAD_REQUEST,

        # ========== MACHINE ==========
        MachineNotFoundError: status.HTTP_404_NOT_FOUND,
        MachineNameAlreadyExistsError: status.HTTP_409_CONFLICT,
        MachineSerialNumberAlreadyExistsError: status.HTTP_409_CONFLICT,
        InvalidMachineStatusError: status.HTTP_400_BAD_REQUEST,
        MachineAccessDeniedError: status.HTTP_403_FORBIDDEN,
        MachineFetchError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        MachineInvalidNameError: status.HTTP_400_BAD_REQUEST,
        MachineInvalidSerialNumberError: status.HTTP_400_BAD_REQUEST,

        # ========== SHIFT ==========
        ShiftNotFoundError: status.HTTP_404_NOT_FOUND,
        ShiftAlreadyExistsError: status.HTTP_409_CONFLICT,
        ShiftPermissionError: status.HTTP_403_FORBIDDEN,
        ShiftTimeRangeError: status.HTTP_400_BAD_REQUEST,
        ShiftNameIsInvalidError: status.HTTP_400_BAD_REQUEST,
        ShiftStartTimeIsInvalidError: status.HTTP_400_BAD_REQUEST,
        ShiftEndTimeIsInvalidError: status.HTTP_400_BAD_REQUEST,

        # ========== USER ==========
        UserNotFoundError: status.HTTP_404_NOT_FOUND,
        EmailDoesNotExistError: status.HTTP_404_NOT_FOUND,
        PhoneNumberDoesNotExistError: status.HTTP_404_NOT_FOUND,

        InvalidUserIdError: status.HTTP_400_BAD_REQUEST,
        InvalidFullNameError: status.HTTP_400_BAD_REQUEST,
        InvalidEmailError: status.HTTP_400_BAD_REQUEST,
        InvalidPasswordError: status.HTTP_400_BAD_REQUEST,
        InvalidPhoneNumberError: status.HTTP_400_BAD_REQUEST,
        InvalidRoleError: status.HTTP_400_BAD_REQUEST,
        EmptyRoleError: status.HTTP_400_BAD_REQUEST,

        EmailAlreadyExistsError: status.HTTP_409_CONFLICT,
        PhoneNumberAlreadyExistsError: status.HTTP_409_CONFLICT,

        IncorrectPasswordError: status.HTTP_401_UNAUTHORIZED,
        UserAuthenticationError: status.HTTP_401_UNAUTHORIZED,
        UserAuthorizationError: status.HTTP_403_FORBIDDEN,
        UserNotAllowedError: status.HTTP_403_FORBIDDEN,
        MissingPasswordError: status.HTTP_400_BAD_REQUEST,

        UserCreationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        UserUpdateError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        UserDeletionError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        UserFetchError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        PasswordUpdateError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    # Register each exception → response handler
    for exc_class, status_code in exception_to_status.items():

        @app.exception_handler(exc_class)
        async def handler(request: Request, exc: exc_class, status_code=status_code):
            return JSONResponse(
                status_code=status_code,
                content={"error": str(exc)}
            )
