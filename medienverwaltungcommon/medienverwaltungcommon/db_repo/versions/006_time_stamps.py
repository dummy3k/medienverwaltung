from sqlalchemy import *
from migrate import *
import migrate.changeset
from datetime import datetime

meta = MetaData()

media_table = Table('media', meta,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

created_ts = Column('created_ts', DateTime)
updated_ts = Column('updated_ts', DateTime)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    created_ts.create(media_table)
    media_table.update(values={'created_ts':datetime.now()}).execute()

    updated_ts.create(media_table)
    media_table.update(values={'updated_ts':datetime.now()}).execute()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    updated_ts.drop(media_table)
    created_ts.drop(media_table)
