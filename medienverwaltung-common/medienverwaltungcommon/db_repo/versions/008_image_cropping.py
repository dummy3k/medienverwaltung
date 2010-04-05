from sqlalchemy import *
from migrate import *
import migrate.changeset
from datetime import datetime

meta = MetaData(migrate_engine)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

image_crop = Column('image_crop', PickleType)

def upgrade():
    image_crop.create(media_table)

def downgrade():
    image_crop.drop(media_table)
