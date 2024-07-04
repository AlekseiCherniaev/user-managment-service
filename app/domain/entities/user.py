import re
import uuid

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

from app.config.exceptions import InvalidPhoneNumberException


class UserBase(BaseModel):
    name: str
    surname: str
    username: str
    phone_number: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    role_id: int
    group_id: int
    image_path: Optional[str] = Field(None, max_length=128)
    is_blocked: bool = False
    active: bool = True

    @field_validator("phone_number")
    def phone_number_validation(cls, v):
        regex = r"^\+?[1-9][0-9]{7,14}$"
        if not re.fullmatch(regex, v):
            raise InvalidPhoneNumberException
        return v


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserUpdatePartial(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None
    group_id: Optional[int] = None
    image_path: Optional[str] = Field(None, max_length=128)
    is_blocked: Optional[bool] = None
    active: Optional[bool] = None


class User(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
