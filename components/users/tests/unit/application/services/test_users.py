import pytest
from application.services import Users

test_data_user = {
    'name': 'Alex',
    'login': 'alex',
    'password': 'qwerty',
}


@pytest.fixture(scope='function')
def service(user_repo):
    return Users(user_repo=user_repo,)


def test__get_by_id(service, user):
    assert service.get_by_id(1) == user


def test__get_all(service, user):
    assert service.get_all() == [
        user,
    ]


def test__delete_user(service, user):
    assert service.delete_user(1) is None


def test__add_user(service, user):
    assert service.add_user(**test_data_user) is None
