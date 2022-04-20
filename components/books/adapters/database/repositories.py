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

    @staticmethod
    def price_converter(price: str):
        return int(price[1:])

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

    def get_all(self, order_by=None, sort_by=None, price=None, keyword=None, author=None, publisher=None) -> List[Book]:

        query = select(BOOK)
        if price:
            query = query.where(BOOK.c.price == price)

        if keyword:
            search = "%{}%".format(keyword)
            query = query.where(BOOK.c.title.like(search))

        if author:
            query = query.where(BOOK.c.author == author)

        if publisher:
            query = query.where(BOOK.c.publisher == publisher)

        if order_by and sort_by:
            if order_by == 'asc':
                if sort_by == 'price':
                    query = query.order_by(asc(BOOK.c.price))
                elif sort_by == 'pages':
                    query = query.order_by(asc(BOOK.c.pages))
            elif order_by == 'desc':
                if sort_by == 'price':
                    query = query.order_by(desc(BOOK.c.price))
                elif sort_by == 'pages':
                    query = query.order_by(desc(BOOK.c.pages))

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
        return res

    def get_active(self, id_user: int):
        res = self.session.query(BOOK.c.title).filter(
            BOOK.c.owner == id_user, BOOK.c.is_bought == False).all()
        return res
