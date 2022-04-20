from unittest.mock import Mock

import pytest

from application import interfaces


@pytest.fixture(scope='function')
def user_repo(user):
    user_repo = Mock(interfaces.UsersRepo)
    user_repo.get_by_id = Mock(return_value=user)
    user_repo.add_user = Mock(return_value=None)
    user_repo.delete_user = Mock(return_value=None)
    user_repo.get_all = Mock(return_value=[user, ])
    return user_repo

