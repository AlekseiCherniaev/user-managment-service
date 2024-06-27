from abc import ABC, abstractmethod
from typing import Optional, Sequence

from app.domain.entities.user import User


class BaseRepo(ABC):
    @abstractmethod
    def create(self, user: User, session) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_id(self, user_id: int, session) -> Optional[User]:
        ...

    @abstractmethod
    def list(self, session) -> Optional[Sequence[User]]:
        ...

    @abstractmethod
    def update(self, user_id: User, session) -> User:
        ...

    @abstractmethod
    def delete(self, user_id, session):
        ...
