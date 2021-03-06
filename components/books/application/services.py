from datetime import datetime
from typing import List, Optional

from evraz.classic.app import DTO
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import Message, Publisher
from pydantic import validate_arguments

from . import interfaces
from .dataclasses import Book
from .exceptions import NotAvailable, NotFound

join_points = PointCut()
join_point = join_points.join_point


class BookInfo(DTO):
    id: int
    title: str
    subtitle: str
    authors: str
    publisher: str
    isbn10: str
    isbn13: str
    pages: int
    year: int
    rating: int
    desc: str
    price: str
    language: str
    expiration_date: Optional[datetime] = None
    owner: Optional[int] = None
    is_bought: Optional[bool] = None
    image: Optional[str]
    url: Optional[str]
    error: Optional[str] = None


@component
class Books:
    book_repo: interfaces.BooksRepo
    publisher: Optional[Publisher] = None
    user_publisher: Optional[Publisher] = None

    @join_point
    @validate_arguments
    def get_by_id(self, id: int):
        book = self.book_repo.get_by_id(id)
        if not book:
            raise NotFound
        return book

    @join_point
    def add_book(self, data: dict):
        book = Book(**data)
        self.book_repo.add_instance(book)

    @join_point
    @validate_arguments
    def take_book(self, id_book: int, id_user: int, days: int):
        book = self.book_repo.get_by_id(id_book)

        if (book.expiration_date is None or book.expiration_date < datetime.now()) and (book.owner is None or
                                                                                        book.owner == id_user):
            self.book_repo.take_book(id_book=id_book, id_user=id_user, days=days)
            self.book_repo.add_to_log(id_book=id_book, id_user=id_user)
        else:
            raise NotAvailable

    @join_point
    @validate_arguments
    def return_book(self, id_book: int, id_user: int):
        book = self.book_repo.get_by_id(id_book)

        if id_user == book.owner:
            self.book_repo.return_book(id_book=id_book)

    @join_point
    @validate_arguments
    def buy_book(self, id_book: int, id_user: int):

        book = self.book_repo.get_by_id(id_book)

        if book.owner == id_user and not book.is_bought:
            self.book_repo.buy_book(id_book=id_book, id_user=id_user)
        else:
            raise NotAvailable

    @join_point
    @validate_arguments
    def get_history(self, id_user: int):
        books = self.book_repo.get_history(id_user)
        return books

    @join_point
    @validate_arguments
    def get_active(self, id_user: int):
        books = self.book_repo.get_active(id_user)
        return books

    @join_point
    def send_to_users(self, sep_ids):
        for ids in sep_ids:
            books = self.book_repo.get_top3(ids)
            titles = []
            for book in books:
                titles.append(book.title)
            self.user_publisher.publish(Message('queue', {'books': titles}))

    @join_point
    def get_all(self, params) -> List[Book]:
        order_by = None
        sort_by = None
        price = None
        keyword = None
        author = None
        publisher = None
        if 'order_by' and 'sort_by' in params:
            order_by = params['order_by']
            sort_by = params['sort_by']
        if 'price' in params:
            price = params['price']
        if 'keyword' in params:
            keyword = params['keyword']
        if 'author' in params:
            author = params['author']
        if 'publisher' in params:
            publisher = params['publisher']

        books = self.book_repo.get_all(order_by, sort_by, price, keyword, author, publisher)
        return books
