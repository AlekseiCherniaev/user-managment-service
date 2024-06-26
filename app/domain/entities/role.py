import enum

from pydantic import BaseModel
from typing import Optional


class RoleEnum(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class RoleBase(BaseModel):
    name: RoleEnum


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleUpdatePartial(BaseModel):
    name: Optional[RoleEnum] = None


class Role(RoleBase):
    id: int
