import pytest

from application.services import Books


@pytest.fixture(scope='function')
def service(book_repo):
    return Books(book_repo=book_repo, )


def test__get_all(service, book):
    assert service.get_all([None]) == [
        book,
    ]


def test__get_by_id(service, book):
    assert service.get_by_id(1) == book


def test__take_book(service, book):
    assert service.take_book(1, 1, 10) is None


def test__return_book(service, book):
    assert service.return_book(1, 1) is None


def test__buy_book(service, book):
    assert service.buy_book(1, 1) is None


def test__get_history(service, book):
    assert service.get_history(1) == [
        book,
    ]


def test__get_active(service, book):
    assert service.get_active(1) == [
        book,
    ]
