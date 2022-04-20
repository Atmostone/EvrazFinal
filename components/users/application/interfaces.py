from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import User


class UsersRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[User]: ...

    @abstractmethod
    def add_user(self, user: User): ...

    @abstractmethod
    def get_all(self) -> List[User]: ...

    @abstractmethod
    def delete_instance(self, id_: int): ...

    @abstractmethod
    def login_user(self, login: str) -> Optional[User]: ...
