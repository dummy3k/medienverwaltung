from sqlalchemy import *
from migrate import *

meta = MetaData()

media_table = Table('media', meta,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    media_table.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    media_table.drop()
