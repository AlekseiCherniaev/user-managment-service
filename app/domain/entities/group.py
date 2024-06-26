from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GroupBase(BaseModel):
    name: str = Field(max_length=52)


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class GroupUpdatePartial(BaseModel):
    name: Optional[str] = Field(None, max_length=52)


class Group(GroupBase):
    id: int
    created_at: datetime
