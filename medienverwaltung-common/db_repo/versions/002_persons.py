from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

### New tables

persons_table = Table('persons', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)),
    #~ Column('wikipedia_url', Unicode(255)),
    #~ Column('image_url', Unicode(255)),
)

relation_types_table = Table('relation_types', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)), # Actor, Director, Manufacturer
)

media_to_asin_table = Table('media_to_asin', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('media_id', Integer, ForeignKey('media.id')),
    Column('asin', Unicode(10)),
)

person_to_media_table = Table('person_to_media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('person_id', Integer, ForeignKey('persons.id')),
    Column('medium_id', Integer, ForeignKey('media.id')),
    Column('type_id', Integer, ForeignKey('relation_types.id')),
)

def upgrade():
    persons_table.create()
    relation_types_table.create()
    media_to_asin_table.create()
    person_to_media_table.create()

    inserter = relation_types_table.insert()
    inserter.execute(name=u'Actor')
    inserter.execute(name=u'Director')
    inserter.execute(name=u'Manufacturer')

def downgrade():
    persons_table.drop()
    relation_types_table.drop()
    media_to_asin_table.drop()
    person_to_media_table.drop()
