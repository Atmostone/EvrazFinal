from adapters.database import tables
from application import dataclasses
from sqlalchemy.orm import registry

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.USER)
