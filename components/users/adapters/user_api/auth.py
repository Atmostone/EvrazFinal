import jwt
from evraz.classic.http_auth import Group, Permission, strategies


class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    USERS = Group('User', permissions=(Permissions.FULL_CONTROL,))


jwt_strategy = strategies.JWT(secret_key='my_secret_jwt')

ALL_GROUPS = (Groups.USERS,)


def generate_token(user) -> str:
    token = jwt.encode({
        'sub': user.id,
        'login': user.login,
        'name': user.name,
        'group': 'User'
    },
        'my_secret_jwt',
        algorithm='HS256')
    return token
