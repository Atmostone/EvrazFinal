from sqlalchemy.orm import registry

from application import dataclasses
from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.Book, tables.BOOK)
