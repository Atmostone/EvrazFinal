import sys

from evraz.classic.messaging_kombu import KombuPublisher
from evraz.classic.sql_storage import TransactionContext
from kombu import Connection
from sqlalchemy import create_engine

from adapters import book_api, database, message_bus
from adapters.books_loader import Loader
from application import services



class Settings:
    db = database.Settings()
    book_api = book_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    books_repo = database.repositories.BooksRepo(context=context)


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
        messages_params={
            'queue': {
                'exchange': 'exchange',
            }
        }, )


class Application:
    is_dev_mode = Settings.book_api.IS_DEV_MODE
    books = services.Books(book_repo=DB.books_repo)



def load_books(tags, publisher):
    loader = Loader(books_service=Application.books)
    loader.load(tags, publisher)


if __name__ == '__main__':
    print(1)
    print(sys.argv[1:])
    load_books(sys.argv[1:], publisher=MessageBus.publisher)
    print(2)
