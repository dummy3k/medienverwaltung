if __name__ == '__main__':
    import logging.config
    logging.config.fileConfig("settings.conf")

import amazonproduct
import ConfigParser
from optfunc import optfunc
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import select, join, and_, or_, not_
import urllib
from StringIO import StringIO
import logging
import os

import helper as h
import medienverwaltungweb.model as model
from medienverwaltungcommon.amazon import add_persons, RefHelper

log = logging.getLogger(__name__)

config = ConfigParser.ConfigParser()
config.read('settings.conf')

api = amazonproduct.API(config.get('Amazon', 'AccessKeyID'),
                        config.get('Amazon', 'SecretAccessKey'))
SearchIndex='Books'

engine = create_engine(config.get('sqlalchemy', 'url'))
session = scoped_session(sessionmaker())
session.configure(bind=engine)

type = "dvd"


def variant001():
    tag_query = select([model.tags_table.c.name], from_obj=[
        model.tags_table.join(model.media_table)\
                        .join(model.media_types_table)
                        .join(model.media_types_table.alias('sub'))
    ]).where(model.media_types_table.c.name==type)\
      .where(model.tags_table.c.name==u'scifi')\
      .distinct()

    tag_query.bind = engine
    result = map(lambda x: x[0], tag_query.execute())
    print result
    
def variant002():
    tag_name = 'scifi'
    
    sub_tags_table = model.tags_table.alias('sub')
    tag_query = select([model.tags_table.c.name], from_obj=[
        model.tags_table.join(model.media_table)\
                        .join(sub_tags_table)
    ]).where(sub_tags_table.c.name==tag_name)\
      .distinct()
    #~ h.ipython()()
    print tag_query
    
    tag_query.bind = engine
    result = map(lambda x: x[0], tag_query.execute())
    print result

def variant003():
    #~ tag_name = u'test'
    tag_name = None
    media_type_name = 'book'
    media_type_name = None

    join_clause = model.tags_table.join(model.media_table)

    if tag_name:
        sub_tags_table = model.tags_table.alias('sub_tags')
        join_clause = join_clause.join(sub_tags_table)

    if media_type_name:
        sub_media_types_table = model.media_types_table.alias('sub_media_types_table')
        join_clause = join_clause.join(sub_media_types_table)

    tag_query = select([model.tags_table.c.name], from_obj=[join_clause])

    if tag_name:
        tag_query = tag_query.where(sub_tags_table.c.name==tag_name)
        
    if media_type_name:
        tag_query = tag_query.where(sub_media_types_table.c.name==media_type_name)
        
    tag_query = tag_query.distinct()
    print tag_query
    
    tag_query.bind = engine
    result = map(lambda x: x[0], tag_query.execute())
    for item in result:
        print item
    #~ print result

def variant004():
    t = model.media_table
    foo = model.media_table.c.created_ts
    t.update(values={'created_ts':datetime.now()})
    h.ipython()()
    pass

def variant005():
    query = u"%term%"
    media_query = session\
                      .query(model.Medium)\
                      .filter(model.Medium.title.like(query))
    h.ipython()()
    pass

variant005()
