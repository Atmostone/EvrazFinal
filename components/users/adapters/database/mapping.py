from sqlalchemy.orm import registry

from adapters.database import tables
from application import dataclasses

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.USER)
