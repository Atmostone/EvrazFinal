import datetime

import requests
from evraz.classic.aspects import PointCut
from evraz.classic.messaging import Message

join_points = PointCut()
join_point = join_points.join_point


class Loader:
    books_ids = []
    books_data = []

    def __init__(self, books_service):
        self.books_service = books_service

    @join_point
    def load(self, tags, publisher):
        for tag in tags:
            ids = []

            response = requests.get(f'https://api.itbook.store/1.0/search/{tag}', verify=False).json()

            total = int(response.get('total'))

            books_amount = total // 10 + int((total % 10) > 0)

            if books_amount < 5:
                books_amount = books_amount
            else:
                books_amount = 5

            for i in range(1, books_amount + 1):
                request_data = requests.get(f'https://api.itbook.store/1.0/search/{tag}/{i}', verify=False).json()
                for book in request_data.get('books'):
                    ids.append(book.get('isbn13'))
                    print(book.get('isbn13'))

            for id in ids:
                response = requests.get(f'https://api.itbook.store/1.0/books/{id}', verify=False).json()


                print(response)

                publisher.publish(
                    Message(
                        'queue',
                        {
                            'data': response
                        })
                )
