from sqlalchemy import *
from migrate import *

meta = MetaData()

media_table = Table('media', meta,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
)

# new tables & columns

users_table = Table('users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)),
    Column('pwd_salt', Integer),
    Column('pwd_hash', Unicode(50)),
    Column('last_login', DateTime),
)

user_openids_table = Table('user_openids', meta,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('openid', Unicode(50)),
)

creator_user_id = Column('creator_user_id', Integer, ForeignKey('users.id'))


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    users_table.create()
    user_openids_table.create()
    creator_user_id.create(media_table)
    #~ media_table.update(values={'creator_user_id':0})

def downgrade(migrate_engine):
    meta.bind = migrate_engine

    creator_user_id.drop(media_table)
    user_openids_table.drop()
    users_table.drop()
