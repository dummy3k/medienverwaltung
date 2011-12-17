from sqlalchemy import *
from migrate import *
import migrate.changeset

meta = MetaData()

media_table = Table('media', meta,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

image_data = Column('image_data', PickleType)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    image_data.create(media_table)

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    # Operations to reverse the above upgrade go here.
    pass
