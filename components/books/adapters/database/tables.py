from sqlalchemy import Boolean, Column, DateTime, Integer, MetaData, String, Table

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)
BOOK = Table(
    'book',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(500)),
    Column('subtitle', String(500)),
    Column('authors', String(350)),
    Column('publisher', String(350)),
    Column('isbn10', String(20)),
    Column('isbn13', String(20)),
    Column('pages', Integer),
    Column('year', Integer),
    Column('rating', Integer),
    Column('desc', String(10000)),
    Column('price', String(35)),
    Column('is_bought', Boolean, default=False),
    Column('image', String(350), nullable=True),
    Column('url', String(350), nullable=True),
    Column('error', String(50), nullable=True),
    Column('language', String(50), nullable=True),
    Column('expiration_date', DateTime, default=None),
    Column('owner', Integer, default=None),
)

LOGBOOK = Table(
    'logbook',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('id_user', Integer),
    Column('id_book', Integer),
)
