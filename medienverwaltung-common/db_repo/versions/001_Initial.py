from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

def upgrade():
    media_table.create()

def downgrade():
    media_table.drop()
