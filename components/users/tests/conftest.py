import pytest

from application import dataclasses


@pytest.fixture
def user():
    return dataclasses.User(
        name='Alex',
        login='alex',
        password='qwerty',
        id=1,
    )
