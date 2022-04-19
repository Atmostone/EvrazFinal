from typing import Optional, List

from evraz.classic.app import DTO, validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from pydantic import validate_arguments
from evraz.classic.messaging import Message, Publisher

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
            raise Exception
        return user

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        new_user = user_info.create_obj(User)
        new_user = self.user_repo.add_instance(new_user)
        return new_user

    @join_point
    @validate_arguments
    def login_user(self, user_login: str, user_password: str):
        user = self.user_repo.get_by_login(user_login)
        if not user:
            raise Exception
        if user.password == user_password:
            return user
        else:
            raise Exception

    @join_point
    @validate_arguments
    def delete_user(self, id: int):
        user = self.user_repo.get_by_id(id)
        if not user:
            raise Exception
        self.user_repo.delete_instance(id)


    @join_point
    def get_all(self) -> List[User]:
        users = self.user_repo.get_all()
        return users
