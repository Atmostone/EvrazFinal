import sys

from adapters.books_loader import Loader
from composites.book_api import DB
from evraz.classic.messaging_kombu import KombuPublisher
from kombu import Connection

from adapters import book_api, database, message_bus
from application import services


class Settings:
    db = database.Settings()
    book_api = book_api.Settings()
    message_bus = message_bus.Settings()


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
        messages_params={'queue': {
            'exchange': 'exchange',
            'routing_key': 'books',
        }},
    )

    user_publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
        messages_params={'queue': {
            'exchange': 'exchange',
            'routing_key': 'users',
        }},
    )


class Application:
    is_dev_mode = Settings.book_api.IS_DEV_MODE
    books = services.Books(
        book_repo=DB.books_repo, publisher=MessageBus.publisher, user_publisher=MessageBus.user_publisher
    )


def load_books(tags, publisher):
    loader = Loader(books_service=Application.books)
    ids = loader.load(tags, publisher)
    Application.books.send_to_users(ids)


if __name__ == '__main__':
    load_books(sys.argv[1:], publisher=MessageBus.publisher)
