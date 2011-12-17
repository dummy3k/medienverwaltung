from sqlalchemy import *
from migrate import *

meta = MetaData()

media_table = Table('media', meta,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

### New tables

borrowers_table = Table('borrowers', meta,
    Column('id', Integer, primary_key=True),
    Column('first_name', Unicode(50)),
    Column('last_name', Unicode(50)),
    Column('email', Unicode(50)),
    Column('created_ts', DateTime),
    Column('updated_ts', DateTime),
)

borrow_acts_table = Table('borrow_acts', meta,
    Column('id', Integer, primary_key=True),
    Column('media_id', Integer, ForeignKey('media.id')),
    Column('borrower_id', Integer, ForeignKey('borrowers.id')),
    Column('borrowed_ts', DateTime),
    Column('returned_ts', DateTime),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    borrowers_table.create()
    borrow_acts_table.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    borrow_acts_table.drop()
    borrowers_table.drop()
