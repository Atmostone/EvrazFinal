from datetime import datetime, timedelta
from typing import List, Optional

from application import interfaces
from application.dataclasses import Book, LogBook
from .tables import BOOK, LOGBOOK
from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository
from sqlalchemy import select, update, desc, asc, insert


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

    def return_book(self, id_book: int):
        query = update(BOOK).where(BOOK.c.id == id_book).values(owner=None, expiration_date=None)
        return self.session.execute(query)

    def buy_book(self, id_book: int, id_user: int):
        query = update(BOOK).where(BOOK.c.id == id_book).values(owner=id_user, expiration_date=None, is_bought=True)
        return self.session.execute(query)

    def take_book(self, id_book: int, id_user: int, days: int):
        query = update(BOOK).where(BOOK.c.id == id_book).values(owner=id_user,
                                                                expiration_date=datetime.now() + timedelta(days=days))
        return self.session.execute(query)

    def add_to_log(self, id_book: int, id_user: int):
        query = insert(LOGBOOK).values(id_book=id_book, id_user=id_user)
        self.session.execute(query)

    def get_from_log(self, id_user: int):
        res = self.session.query(BOOK.c.title).join(LOGBOOK, BOOK.c.id == LOGBOOK.c.id_book).filter(
            LOGBOOK.c.id_user == id_user).all()
        print('!!!!!', res)
        # query = select(LOGBOOK.c.id_book).where(LOGBOOK.c.id_user == id_user)
        # ids = self.session.execute(query).fetchall()
        # print('AAAAAAAAA', ids)
        # query2 = select(BOOK.c.title).where(BOOK.c.id.in_(ids))
        #
        # res = self.session.execute(query2).fetchall()
        return res
