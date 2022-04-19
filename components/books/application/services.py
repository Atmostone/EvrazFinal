import json
from typing import Optional, List

from evraz.classic.app import DTO
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import Message, Publisher
from pydantic import validate_arguments

from . import interfaces
from .dataclasses import Book

join_points = PointCut()
join_point = join_points.join_point


class BookInfo(DTO):
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
    image: Optional[str]
    url: Optional[str]
    id: Optional[int] = None
    error: Optional[str] = None


@component
class Books:
    book_repo: interfaces.BooksRepo
    publisher: Optional[Publisher] = None
    user_publisher: Optional[Publisher] = None

    @join_point
    @validate_arguments
    def get_info(self, id: int):
        book = self.book_repo.get_by_id(id)
        if not book:
            raise Exception
        return book

    @join_point
    def add_book(self, data: dict):
        book = Book(**data)
        self.book_repo.add_instance(book)

    @join_point
    def send_to_users(self, sep_ids):
        for ids in sep_ids:
            books = self.book_repo.get_top3(ids)
            print(books)
            titles = []
            for book in books:
                titles.append(book.title)
            self.user_publisher.publish(
                Message('queue',
                        {
                            'books': titles
                        })
            )
            print('Send', titles)

    @join_point
    @validate_arguments
    def delete_book(self, id: int):
        book = self.book_repo.get_by_id(id)
        if not book:
            raise Exception
        self.book_repo.delete_instance(id)

    @join_point
    def get_all(self) -> List[Book]:
        books = self.book_repo.get_all()
        return books

    @join_point
    @validate_arguments
    def return_book(self, book_id: int, user_id: int):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception
        if book.user_id == user_id:
            self.book_repo.return_book(book_id)
        else:
            raise Exception

    @join_point
    @validate_arguments
    def take_book(self, book_id: int, user_id: int):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception
        if book.user_id is None:
            self.book_repo.take_book(book_id=book_id, user_id=user_id)
        else:
            raise Exception
