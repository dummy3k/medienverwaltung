from sqlalchemy import *
from migrate import *
import migrate.changeset

meta = MetaData()

media_table = Table('media', meta,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

### New tables and columns
#~ if migrate_engine.name == 'sqlite':
    #~ media_type_id_colum = Column('media_type_id', Integer)
#~ else:
    #~ media_type_id_colum = Column('media_type_id', Integer, ForeignKey('media_types.id'))
media_type_id_colum = Column('media_type_id', Integer, ForeignKey('media_types.id'))

isbn_colum = Column('isbn', Unicode(15))

media_types_table = Table('media_types', meta,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)),
    Column('amzon_search_index', Unicode(10)),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    media_types_table.create()
    media_type_id_colum.create(media_table)
    isbn_colum.create(media_table)

    inserter = media_types_table.insert()
    inserter.execute(name=u'book', amzon_search_index=u'Books')
    inserter.execute(name=u'dvd', amzon_search_index=u'DVD')

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    media_type_id_colum.drop(media_table)
    isbn_colum.drop(media_table)
    media_types_table.drop()
