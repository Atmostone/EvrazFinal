from typing import List, Optional

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository
from sqlalchemy import desc, select

from application import interfaces
from application.dataclasses import User
from .tables import USER


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):

    def get_by_id(self, user_id: int) -> Optional[User]:
        query = select(USER).where(USER.c.id == user_id)
        result = self.session.execute(query).fetchone()
        return result

    def add_user(self, user: User):
        query = USER.insert().values(name=user.name, login=user.login, password=user.password)
        self.session.execute(query)
        new_user = select(USER).order_by(desc(USER.c.id))
        new_user = self.session.execute(new_user).fetchone()
        return new_user

    def get_all(self) -> List[User]:
        query = select(USER)
        return self.session.execute(query).fetchall()

    def delete_instance(self, user_id: int):
        query = USER.delete().where(USER.c.id == user_id)
        return self.session.execute(query)

    def login_user(self, user_login: str) -> Optional[User]:
        query = select(USER).where(USER.c.login == user_login)
        result = self.session.execute(query).fetchone()
        return result
