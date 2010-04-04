from sqlalchemy import *
#~ from medienverwaltungweb.model import meta
import meta

tags_table = Table('tags', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(100)),
    Column('media_id', Integer, ForeignKey('media.id')),
)

class Tag(object):
    def __unicode__(self):
        return "<Tag(%s, '%s')>" % (self.id, self.name)

    #~ __str__ = __unicode__

    def __repr__(self):
        return self.__unicode__().encode('ascii', 'replace')
