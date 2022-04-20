import json
from datetime import datetime, date

from evraz.classic.components import component
from evraz.classic.http_auth import authenticate, authenticator_needed

from application import services
from .join_points import join_point


@authenticator_needed
@component
class Books:
    books: services.Books

    @join_point
    @authenticate
    def on_get_show_info(self, request, response):
        book = self.books.get_by_id(**request.params)
        response.media = {
            'id': book.id,
            'title': book.title,
            'subtitle': book.subtitle,
            'authors': book.authors,
            'publisher': book.publisher,
            'isbn10': book.isbn10,
            'isbn13': book.isbn13,
            'pages': book.pages,
            'year': book.year,
            'rating': book.rating,
            'desc': book.desc,
            'price': book.price,
            'language': book.language,
            'is_bought': book.is_bought,
            'expiration_date': str(book.expiration_date),
            'owner': book.owner,
        }

    @join_point
    @authenticate
    def on_post_take_book(self, request, response):
        self.books.take_book(**request.media)
        response.media = {
            'message': 'Вы успешно взяли книгу'
        }

    @join_point
    @authenticate
    def on_post_return_book(self, request, response):
        self.books.return_book(**request.media)
        response.media = {
            'message': 'Вы успешно вернули книгу'
        }

    @join_point
    @authenticate
    def on_post_buy_book(self, request, response):
        self.books.buy_book(**request.media)
        response.media = {
            'message': 'Вы успешно купили книгу'
        }

    @join_point
    @authenticate
    def on_get_show_history(self, request, response):
        id_user = request.get_param_as_int('id_user')
        books = self.books.get_history(id_user)

        response.media = {
            'books': str(books)
        }

    @join_point
    @authenticate
    def on_get_active_books(self, request, response):
        id_user = request.get_param_as_int('id_user')
        books = self.books.get_active(id_user)

        response.media = {
            'books': str(books)
        }

    @join_point
    @authenticate
    def on_get_show_all(self, request, response):
        books = self.books.get_all(request.params)
        response.media = [{
                        'id': book.id,
            'title': book.title,
            'subtitle': book.subtitle,

            'authors': book.authors,
            'publisher': book.publisher,

            'isbn10': book.isbn10,
            'isbn13': book.isbn13,
            'pages': book.pages,
            'year': book.year,
            'rating': book.rating,
            'desc': book.desc,
            'price': book.price,
            'language': book.language,
            'is_bought': book.is_bought,
            'expiration_date': str(book.expiration_date),
            'owner': book.owner,
        } for book in books]


"Фильтр по цене  /ключевому слову/автору  /издателю. Сортировка по цене/размеру."
