from sqlalchemy import *
from migrate import *
#~ import migrate.changeset

meta = MetaData()

persons_table = Table('persons', meta,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)),
)

### New tables

person_aliases_table = Table('person_aliases', meta,
    Column('id', Integer, primary_key=True),
    Column('person_id', Integer, ForeignKey('persons.id')),
    Column('name', Unicode(50)),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    person_aliases_table.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    person_aliases_table.drop()
