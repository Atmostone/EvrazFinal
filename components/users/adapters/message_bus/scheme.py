from kombu import Exchange, Queue

from evraz.classic.messaging_kombu import BrokerScheme

broker_scheme = BrokerScheme(
    Queue('UserQueue', Exchange('exchange'), routing_key='users', max_length=100)
)
