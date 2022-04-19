from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import Book


class BooksRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[Book]: ...

    @abstractmethod
    def add_instance(self, book: Book): ...

    @abstractmethod
    def get_all(self) -> List[Book]: ...

    @abstractmethod
    def delete_instance(self, id_: int): ...

    @abstractmethod
    def return_book(self, id_book: int, ): ...

    @abstractmethod
    def take_book(self, id_book: int, id_user: int, days: int): ...

    @abstractmethod
    def get_from_log(self, id_user: int): ...

    @abstractmethod
    def add_to_log(self, id_book: int, id_user: int): ...

    @abstractmethod
    def buy_book(self, id_book: int, id_user: int): ...

    @abstractmethod
    def get_top3(self, ids): ...

    @abstractmethod
    def get_active(self, id_user: int): ...
