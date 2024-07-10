from pydantic import BaseModel, Field
from datetime import datetime


class GroupBase(BaseModel):
    name: str = Field(max_length=52)
    created_at: datetime
    updated_at: datetime


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int

