from unittest.mock import Mock

import pytest

from application import interfaces


@pytest.fixture(scope='function')
def books_repo(book):
    books_repo = Mock(interfaces.BooksRepo)
    books_repo.get_info = Mock(return_value=book)
    books_repo.take_book = Mock(return_value=None)
    books_repo.return_book = Mock(return_value=None)
    books_repo.buy_book = Mock(return_value=None)
    books_repo.get_history = Mock(return_value=[book])
    books_repo.get_all = Mock(return_value=[book])
    return books_repo
