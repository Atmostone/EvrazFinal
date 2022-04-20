import os

from pydantic import BaseSettings


class Settings(BaseSettings):

    @property
    def DB_URL(self):
        PG_USER = os.getenv('POSTGRES_USER', 'postgres')
        PG_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
        PG_DBNAME = os.getenv('POSTGRES_DBNAME', 'users')
        PG_HOST = os.getenv('POSTGRES_DB_HOST', 'db_postgres')
        PG_PORT = os.getenv('POSTGRES_PORT', '5432')

        return f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"
