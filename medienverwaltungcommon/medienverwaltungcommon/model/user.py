from sqlalchemy import *
import meta

users_table = Table('users', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)),
    Column('pwd_salt', Integer),
    Column('pwd_hash', Unicode(50)),
    Column('last_login', DateTime),
)

user_openids_table = Table('user_openids', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('openid', Unicode(50)),
)

class User(object):
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return "<User(%s, '%s')>" % (self.id, self.name)

class UserOpenId(object):
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return "<UserOpenId(%s, '%s')>" % (self.id, self.openid)
