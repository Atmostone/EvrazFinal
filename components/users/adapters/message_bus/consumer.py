from application import services
from evraz.classic.messaging_kombu import KombuConsumer
from kombu import Connection

from .scheme import broker_scheme


def create_consumer(connection: Connection, user: services.Users) -> KombuConsumer:
    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        user.print_books,
        'UserQueue',
    )

    return consumer
