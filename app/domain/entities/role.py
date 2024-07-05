import datetime
import enum

from pydantic import BaseModel


class RoleEnum(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class RoleBase(BaseModel):
    name: RoleEnum
    created_at: datetime
    updated_at: datetime


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
