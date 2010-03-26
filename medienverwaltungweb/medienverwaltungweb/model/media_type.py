from sqlalchemy import *
from medienverwaltungweb.model import meta

media_types_table = Table('media_types', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('amzon_search_index', String(10)),
)

class MediaType(object):
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return "<MediaType(%s, '%s')>" % (self.id, self.name)


