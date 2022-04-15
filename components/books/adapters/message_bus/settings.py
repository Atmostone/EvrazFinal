import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    BROKER_URL: str = f'amqp://' \
                      f"{os.getenv('RABBITMQ_USER', 'user')}:" \
                      f"{os.getenv('RABBITMQ_PASSWORD', 'password')}@" \
                      f"{os.getenv('RABBITMQ_HOST', 'rabbitmq')}:" \
                      f"{os.getenv('RABBITMQ_PORT', 5672)}"
