from adapters import database, message_bus, user_api
from application import services
from evraz.classic.messaging_kombu import KombuPublisher
from evraz.classic.sql_storage import TransactionContext
from kombu import Connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Settings:
    db = database.Settings()
    user_api = user_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)
    Session = sessionmaker(bind=engine)
    users_repo = database.repositories.UsersRepo(context=context)


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
    is_dev_mode = Settings.user_api.IS_DEV_MODE
    users = services.Users(user_repo=DB.users_repo, publisher=MessageBus.publisher)


class Aspects:
    services.join_points.join(DB.context)
    user_api.join_points.join(MessageBus.publisher, DB.context)


app = user_api.create_app(
    is_dev_mode=Application.is_dev_mode,
    users=Application.users,
)
