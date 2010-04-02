from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

### New tables

borrowers_table = Table('borrowers', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', Unicode(50)),
    Column('last_name', Unicode(50)),
    Column('email', Unicode(50)),
    Column('created_ts', DateTime),
    Column('updated_ts', DateTime),
)

borrow_history_table = Table('borrow_history', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('media_id', Integer, ForeignKey('media.id')),
    Column('borrower_id', Integer, ForeignKey('borrowers.id')),
    Column('borrowed_ts', DateTime),
    Column('returned_ts', DateTime),
)

def upgrade():
    borrowers_table.create()
    borrow_history_table.create()

def downgrade():
    borrow_history_table.drop()
    borrowers_table.drop()
