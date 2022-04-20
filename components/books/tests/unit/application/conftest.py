from unittest.mock import Mock

import pytest
from application import interfaces


@pytest.fixture(scope='function')
def book_repo(book):
    book_repo = Mock(interfaces.BooksRepo)
    book_repo.get_by_id = Mock(return_value=book)
    book_repo.take_book = Mock(return_value=None)
    book_repo.return_book = Mock(return_value=None)
    book_repo.buy_book = Mock(return_value=None)
    book_repo.get_history = Mock(return_value=[book])
    book_repo.get_all = Mock(return_value=[book])
    book_repo.get_active = Mock(return_value=[book])
    return book_repo
