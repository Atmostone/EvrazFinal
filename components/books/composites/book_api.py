from adapters import book_api, database, message_bus
from application import services
from evraz.classic.messaging_kombu import KombuPublisher
from evraz.classic.sql_storage import TransactionContext
from kombu import Connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Settings:
    db = database.Settings()
    book_api = book_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    books_repo = database.repositories.BooksRepo(context=context)


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


class Aspects:
    services.join_points.join(DB.context)
    book_api.join_points.join(MessageBus.publisher, DB.context)


app = book_api.create_app(
    is_dev_mode=Application.is_dev_mode,
    books=Application.books,
)
