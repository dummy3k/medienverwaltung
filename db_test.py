if __name__ == '__main__':
    import logging.config
    logging.config.fileConfig("settings.conf")

import amazonproduct
import ConfigParser
from optfunc import optfunc
from sqlalchemy import create_engine, func
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
    tag_name = u'test'
    #~ tag_name = None
    #~ media_type_name = 'book'
    media_type_name = None

    join_clause = model.tags_table.join(model.media_table)

    if tag_name:
        sub_tags_table = model.tags_table.alias('sub_tags')
        join_clause = join_clause.join(sub_tags_table)

    if media_type_name:
        sub_media_types_table = model.media_types_table.alias('sub_media_types_table')
        join_clause = join_clause.join(sub_media_types_table)

    cnt_col = func.count()
    tag_query = select([model.tags_table.c.name, cnt_col], from_obj=[join_clause])
    #~ tag_query = select([model.tags_table.c.name], from_obj=[join_clause])

    if tag_name:
        tag_query = tag_query.where(sub_tags_table.c.name==tag_name)
        tag_query = tag_query.where(model.tags_table.c.name != tag_name)
        
    if media_type_name:
        tag_query = tag_query.where(sub_media_types_table.c.name==media_type_name)
        
    #~ tag_query = tag_query.distinct()
    tag_query = tag_query.group_by(model.tags_table.c.name)\
                         .order_by(cnt_col.desc())
    print tag_query
    
    tag_query.bind = engine
    #~ result = map(lambda x: x[0], tag_query.execute())
    result = map(lambda x: (x[0], x[1]), tag_query.execute())
    for item in result:
        print item

def variant004():
    t = model.media_table
    foo = model.media_table.c.created_ts
    t.update(values={'created_ts':datetime.now()})
    h.ipython()()

def variant005():
    query = u"%term%"
    query2 = u"%matrix%"
    media_query = session\
                      .query(model.Medium)\
                      .filter(or_(model.Medium.title.like(query),
                                  model.Medium.title.like(query2)))
                      
    print media_query
    #~ h.ipython()()
    dump_results(media_query.all())

def dump_results(r):
    for item in r:
        print item
        
def variant006():
    tag_query = select([model.tags_table.c.name, func.count()])
    tag_query = tag_query.group_by(model.tags_table.c.name)
    tag_query.bind = engine
    dump_results(tag_query.execute())
    #~ h.ipython()()

def variant007():
    medium_id = 317
    item = session.query(model.Medium)\
                  .filter(model.Medium.id == medium_id)\
                  .first()
                      
    #~ print query
    h.ipython()()
    #~ dump_results(media_query.all())

def variant008():
    medium_id = 306
    query1 = select([model.tags_table.c.name])
    query1 = query1.where(model.tags_table.c.media_id == medium_id)
    print "%s\n" % query1

    cnt_col = func.count()
    query = select([model.tags_table.c.name, cnt_col], from_obj=[model.tags_table])
    query = query.where(model.tags_table.c.name.in_(query1))
    query = query.group_by(model.tags_table.c.name)
    query = query.order_by(cnt_col.desc())
    print "%s\n" % query

    query.bind = engine
    dump_results(query.execute())
    #~ h.ipython()()

def variant009():
    tag_name = u'test'
    #~ tag_name = None
    #~ media_type_name = 'book'
    media_type_name = None


    join_clause = model.tags_table.join(model.media_table)
    if tag_name:
        sub_tags_table = model.tags_table.alias('sub_tags')
        join_clause = join_clause.join(sub_tags_table)

    query1 = select([model.tags_table.c.name],
                       from_obj=[join_clause])

    print query1

def foo(a, b, c):
    print "a: %s, b: %s, c: %s" % (a, b, c)
        
#~ variant009()

args = (12, 34)
foo(*args, c=56)
