from fastapi import HTTPException, status


class BException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidPhoneNumberException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Phone number is not valid"
