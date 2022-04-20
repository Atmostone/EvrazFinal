from typing import Optional, List

from evraz.classic.app import DTO, validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from pydantic import validate_arguments
from evraz.classic.messaging import Message, Publisher

from application.exceptions import NotFound, NotAvailable
from . import interfaces
from .dataclasses import User

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    name: str
    login: str
    password: str
    id: Optional[int]


@component
class Users:
    user_repo: interfaces.UsersRepo
    publisher: Optional[Publisher] = None

    @join_point
    @validate_arguments
    def get_info(self, id: int):
        user = self.user_repo.get_by_id(id)
        if not user:
            raise NotFound
        return user

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        new_user = user_info.create_obj(User)
        new_user = self.user_repo.add_instance(new_user)
        return new_user

    @join_point
    def print_books(self, books):
        users = self.user_repo.get_all()
        for user in users:
            print(f'Send top 3 books to user {user.name}: {books}')

    @join_point
    @validate_arguments
    def login_user(self, user_login: str, user_password: str):
        user = self.user_repo.get_by_login(user_login)
        if not user:
            raise NotFound
        if user.password == user_password:
            return user
        else:
            raise NotAvailable

    @join_point
    @validate_arguments
    def delete_user(self, id: int):
        user = self.user_repo.get_by_id(id)
        if not user:
            raise NotFound
        self.user_repo.delete_instance(id)

    @join_point
    def get_all(self) -> List[User]:
        users = self.user_repo.get_all()
        return users
