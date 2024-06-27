class BException(Exception):
    detail = ""

    def __init__(self):
        super().__init__(self.detail)


class InvalidPhoneNumberException(BException):
    detail = "Invalid phone number"
