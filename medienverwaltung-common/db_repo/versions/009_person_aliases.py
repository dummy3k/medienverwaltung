from sqlalchemy import *
from migrate import *
#~ import migrate.changeset

meta = MetaData(migrate_engine)

persons_table = Table('persons', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)),
)

### New tables

person_aliases_table = Table('person_aliases', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('person_id', Integer, ForeignKey('persons.id')),
    Column('name', Unicode(50)),
)

def upgrade():
    person_aliases_table.create()

def downgrade():
    person_aliases_table.drop()
