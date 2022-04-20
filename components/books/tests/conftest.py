import pytest
from application import dataclasses


@pytest.fixture
def book():
    return dataclasses.Book(
        title='Python',
        subtitle='Python book',
        authors='Alex',
        publisher='Prog books',
        isbn10='123456',
        isbn13='123456789',
        pages=500,
        year=2000,
        rating=5,
        desc='Python is so interesting',
        price='$25',
        language='English',
        id=1,
        owner=1
    )
