import requests
from evraz.classic.aspects import PointCut
from evraz.classic.messaging import Message
from evraz.classic.messaging_kombu import KombuPublisher
from pydantic import ValidationError
from multiprocessing.pool import ThreadPool

join_points = PointCut()
join_point = join_points.join_point


class Loader:
    books_ids = []
    books_data = []

    def __init__(self, books_service):
        self.books_service = books_service

    def get_id(self, tag, page):
        response = requests.get(f"https://api.itbook.store/1.0/search/{tag}/{page}").json()
        books = response.get('books')
        for book in books:
            self.books_ids.append([tag, book.get('isbn13')])

    def load_data(self, book_record_data):
        tag, isbn13 = book_record_data
        response = requests.get(f"https://api.itbook.store/1.0/books/{isbn13}").json()
        response['price'] = response['price'][1:]
        response['tag'] = tag
        return response

    @join_point
    def load(self, tags, publisher):
        for tag in tags:
            response = requests.get(f"https://api.itbook.store/1.0/search/{tag}").json()
            total_books = int(response.get('total'))
            total_books_to_load = min(total_books, 50)
            total_pages_to_load = total_books_to_load // 10 + \
                                  int(total_books_to_load % 10)

            for page in range(1, total_pages_to_load + 1):
                self.get_id(tag, page)

        with ThreadPool(5) as p:
            self.books_data = p.map(self.load_data, self.books_ids)
        for book_data in self.books_data:
            try:
                self.books_service.add_book(**book_data)
            except Exception as e:
                print(e)

        publisher.plan(
            Message('queue', {
                'data': 'books'
            })
        )
