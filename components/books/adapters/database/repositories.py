from typing import List, Optional

from application import interfaces
from application.dataclasses import Book
from .tables import BOOK
from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository
from sqlalchemy import select, update


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):

    def get_by_id(self, book_id: int) -> Optional[Book]:
        query = select(BOOK).where(BOOK.c.id == book_id)
        result = self.session.execute(query).fetchone()
        return result


    def add_instance(self, book: Book):
        print('aaa')
        self.session.add(book)
        print('bbb')
        self.session.flush()
        print(book)
        print('ccc')


    def get_all(self) -> List[Book]:
        query = select(BOOK)
        return self.session.execute(query).fetchall()

    def delete_instance(self, book_id: int):
        query = BOOK.delete().where(BOOK.c.id == book_id)
        return self.session.execute(query)

    def return_book(self, book_id: int):
        query = update(BOOK).where(BOOK.c.id == book_id).values(user_id=None)
        return self.session.execute(query)

    def take_book(self, book_id: int, user_id: int):
        query = update(BOOK).where(BOOK.c.id == book_id).values(user_id=user_id)
        return self.session.execute(query)
