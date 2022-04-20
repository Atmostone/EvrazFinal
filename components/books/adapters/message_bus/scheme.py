from evraz.classic.messaging_kombu import BrokerScheme
from kombu import Exchange, Queue

broker_scheme = BrokerScheme(
    Queue('BookQueue', Exchange('exchange'), routing_key='books', max_length=100),
    Queue('UserQueue', Exchange('exchange'), routing_key='users', max_length=100)
)
