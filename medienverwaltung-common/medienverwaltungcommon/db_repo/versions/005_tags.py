from sqlalchemy import *
from migrate import *

import migrate.changeset

meta = MetaData(migrate_engine)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

tags_table = Table('tags', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(100)),
    Column('media_id', Integer, ForeignKey('media.id')),
)

def upgrade():
    tags_table.create()
    
def downgrade():
    tags_table.drop()
