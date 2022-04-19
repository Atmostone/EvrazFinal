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
        book = self.books.get_info(**request.params)
        response.media = {
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
        }

    @join_point
    @authenticate
    def on_post_add_book(self, request, response):
        self.books.add_book(**request.media)
        response.media = {'status': 'book added'}

    @join_point
    @authenticate
    def on_get_show_all(self, request, response):
        books = self.books.get_all()
        response.media = [{
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
        } for book in books]

    @join_point
    @authenticate
    def on_get_delete_book(self, request, response):
        self.books.delete_book(**request.params)
        response.media = {'status': 'book deleted'}

    @join_point
    @authenticate
    def on_post_take_book(self, request, response):
        request.media['user_id'] = request.context.client.user_id
        self.books.take_book(**request.media)
        response.media = {'status': 'ok'}

    @join_point
    @authenticate
    def on_post_return_book(self, request, response):
        request.media['user_id'] = request.context.client.user_id
        self.books.return_book(**request.media)
        response.media = {'status': 'ok'}
