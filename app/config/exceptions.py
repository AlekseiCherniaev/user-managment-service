from fastapi import HTTPException, status


class BException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class PasswordNotValidException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Password is not valid"


class UserAlreadyExistsException(BException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class UserNotFoundException(BException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class InvalidPhoneNumberException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Phone number is not valid"


class WrongPasswordException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Wrong password"


class InvalidTokenException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token error"


class UserInactiveException(BException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User inactive"


class UserBlockedException(BException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User blocked"


class PermissionDeniedException(BException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"
