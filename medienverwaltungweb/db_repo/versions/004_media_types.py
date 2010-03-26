from sqlalchemy import *
from migrate import *
import migrate.changeset

meta = MetaData(migrate_engine)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
)

### New tables and columns
media_type_id = Column('media_type_id', Integer, ForeignKey('media.id'))

media_types_table = Table('media_types', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
)

def upgrade():
    media_types_table.create()
    media_type_id.create(media_table)

def downgrade():
    media_type_id.drop(media_table)
    media_types_table.drop()
