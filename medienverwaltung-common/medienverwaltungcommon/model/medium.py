from sqlalchemy import *
from medienverwaltungweb.model import meta

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
    Column('image_data', PickleType),
    Column('media_type_id', Integer, ForeignKey('media_types.id')),
    Column('isbn', String(15)),
)

class Medium(object):
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return "<Medium(%s, '%s')>" % (self.id, self.title)


