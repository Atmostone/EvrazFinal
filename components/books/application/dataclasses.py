from datetime import datetime
from typing import Optional

import attr


@attr.dataclass
class Book:
    title: str
    subtitle: str
    authors: str
    publisher: str
    isbn10: str
    isbn13: str
    pages: int
    year: int
    rating: int
    desc: str
    price: str
    language: str
    expiration_date: Optional[datetime] = None
    owner: Optional[int] = None
    is_bought: Optional[bool] = None
    image: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None
    id: Optional[int] = None
