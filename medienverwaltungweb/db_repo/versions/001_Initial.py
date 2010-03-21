from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
)

def upgrade():
    # Upgrade operations go here. Don't create your own engine; use the engine
    # named 'migrate_engine' imported from migrate.
    media_table.create()
    pass

def downgrade():
    # Operations to reverse the above upgrade go here.
    media_table.drop()
