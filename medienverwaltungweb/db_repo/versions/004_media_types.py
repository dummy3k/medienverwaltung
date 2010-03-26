from sqlalchemy import *
from migrate import *
import migrate.changeset

meta = MetaData(migrate_engine)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
)

### New tables and columns
media_type_id_colum = Column('media_type_id', Integer, ForeignKey('media_types.id'))
isbn_colum = Column('isbn', String(15))

media_types_table = Table('media_types', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('amzon_search_index', String(10)),
)

def upgrade():
    media_types_table.create()
    media_type_id_colum.create(media_table)
    isbn_colum.create(media_table)

    inserter = media_types_table.insert()
    inserter.execute(name='book', amzon_search_index='books')
    inserter.execute(name='dvd', amzon_search_index='dvd')

def downgrade():
    media_type_id_colum.drop(media_table)
    isbn_colum.drop(media_table)
    media_types_table.drop()
