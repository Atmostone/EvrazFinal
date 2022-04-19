from datetime import datetime, timedelta
from typing import List, Optional

from application import interfaces
from application.dataclasses import Book
from .tables import BOOK
from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository
from sqlalchemy import select, update, desc, asc


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):

    def get_by_id(self, book_id: int) -> Optional[Book]:
        query = select(BOOK).where(BOOK.c.id == book_id)
        result = self.session.execute(query).fetchone()
        return result

    def add_instance(self, book: Book):
        self.session.add(book)
        self.session.flush()

    def get_top3(self, ids):
        return self.session.query(Book).filter(Book.isbn13.in_(ids)).order_by(
            desc(Book.rating), asc(Book.year)).limit(3).all()

    def get_all(self) -> List[Book]:
        query = select(BOOK)
        return self.session.execute(query).fetchall()

    def delete_instance(self, book_id: int):
        query = BOOK.delete().where(BOOK.c.id == book_id)
        return self.session.execute(query)

    def return_book(self, book_id: int):
        query = update(BOOK).where(BOOK.c.id == book_id).values(user_id=None)
        return self.session.execute(query)

    def take_book(self, id_book: int, id_user: int):
        query = update(BOOK).where(BOOK.c.id == id_book).values(owner=id_user,
                                                              expiration_date=datetime.now() + timedelta(days=10))
        return self.session.execute(query)
