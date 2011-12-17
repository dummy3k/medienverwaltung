from sqlalchemy import *
from migrate import *
import migrate.changeset
from datetime import datetime

meta = MetaData()

media_table = Table('media', meta,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

image_crop = Column('image_crop', PickleType)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    image_crop.create(media_table)

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    image_crop.drop(media_table)
