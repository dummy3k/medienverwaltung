if __name__ == '__main__':
    import logging.config
    logging.config.fileConfig("settings.conf")

import logging
import ConfigParser

from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import select, join, and_, or_, not_

import helper as h
import medienverwaltungweb.model as model

log = logging.getLogger(__name__)

config = ConfigParser.ConfigParser()
config.read('settings.conf')

engine = create_engine(config.get('sqlalchemy', 'url'))
session = scoped_session(sessionmaker())
session.configure(bind=engine)

def orphaned_tags():
    query = session.query(model.Tag)
    query = query.filter(not_(model.Tag.media_id.in_(session.query(model.Medium.id))))
    for item in query.all():
        try:
            print item
        except:
            h.ipython()()
            
    

orphaned_tags()

