from sqlalchemy import *
from migrate import *
import migrate.changeset

meta = MetaData(migrate_engine)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
)

image_data = Column('image_data', PickleType)

def upgrade():
    image_data.create(media_table)

def downgrade():
    # Operations to reverse the above upgrade go here.
    pass
