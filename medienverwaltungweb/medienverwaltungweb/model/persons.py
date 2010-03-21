from sqlalchemy import *
from medienverwaltungweb.model import meta

relation_types_table = Table('relation_types', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)), # Actor, Director, Manufacturer
)

persons_table = Table('persons', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    #~ Column('wikipedia_url', String(255)),
    #~ Column('image_url', String(255)),
)

media_to_asin_table = Table('media_to_asin', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('media_id', Integer, ForeignKey('media.id')),
    Column('asin', String(10)),
)

person_to_media_table = Table('person_to_media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('person_id', Integer, ForeignKey('persons.id')),
    Column('medium_id', Integer, ForeignKey('media.id')),
    Column('type_id', Integer, ForeignKey('relation_types.id')),
)

class RelationType(object):
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return "<RelationType(%s, '%s')>" % (self.id, self.name)

class Person(object):
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return "<Person(%s, '%s')>" % (self.id, self.name)


class MediaToAsin(object):
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return "<MediaToAsin(%s, %s -> '%s')>" % (self.id,
                                                  self.media_id,
                                                  self.asin)

class PersonToMedia(object):
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return "<PersonToMedia(%s, %s is %s in/of '%s')>" %\
            (self.id,
             self.person_id,
             self.type_id,
             self.medium_id)

