from sqlalchemy import *
from migrate import *

import migrate.changeset

meta = MetaData()

media_table = Table('media', meta,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

tags_table = Table('tags', meta,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(100)),
    Column('media_id', Integer, ForeignKey('media.id')),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tags_table.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    tags_table.drop()
