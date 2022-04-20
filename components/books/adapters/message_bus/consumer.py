from application import services
from evraz.classic.messaging_kombu import KombuConsumer
from kombu import Connection

from .scheme import broker_scheme


def create_consumer(connection: Connection, book: services.Books) -> KombuConsumer:
    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        book.add_book,
        'BookQueue',
    )

    return consumer
