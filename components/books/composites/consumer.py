from composites.book_api import DB
from kombu import Connection

from adapters import database, message_bus
from application import services


class Settings:
    db = database.Settings()
    message_bus = message_bus.Settings()


class Application:
    books = services.Books(book_repo=DB.books_repo)


class MessageBusCons:
    connection = Connection(Settings.message_bus.BROKER_URL)
    consumer = message_bus.create_consumer(connection, Application.books)

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(MessageBusCons.connection)


if __name__ == '__main__':
    MessageBusCons.declare_scheme()
    MessageBusCons.consumer.run()
