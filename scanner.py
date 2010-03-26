import amazonproduct
import ConfigParser
from optfunc import optfunc
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#~ from sqlalchemy import *

import helper as h
import medienverwaltungweb.model as model

config = ConfigParser.ConfigParser()
config.read('settings.conf')

api = amazonproduct.API(config.get('Amazon', 'AccessKeyID'),
                        config.get('Amazon', 'SecretAccessKey'))
SearchIndex='Books'

engine = create_engine(config.get('sqlalchemy', 'url'))
session = scoped_session(sessionmaker())
session.configure(bind=engine)

def one(isbn):
    print "ISBN: %s" % isbn
    node = api.item_lookup(isbn, IdType='ISBN', SearchIndex=SearchIndex)
    item = node.Items.Item
    #~ h.ipython()()
    title = unicode(item.ItemAttributes.Title)
    #~ title = item.ItemAttributes.Title
    print title

    media_type = session.query(model.MediaType)\
                        .filter(model.MediaType.name == 'book')\
                        .first()
                        

    medium = model.Medium()
    medium.title = title
    medium.media_type_id = media_type.id
    medium.isbn = isbn
    session.add(medium)
    session.commit()

    asin = model.MediaToAsin()
    asin.media_id = medium.id
    asin.asin = item.ASIN
    session.add(asin)
    session.commit()
    
    #~ model.meta.Session.add(record)
    #~ model.meta.Session.commit()

def for_ever():
    while True:
        try:
            user_input = raw_input("ISBN:")
        except KeyboardInterrupt:
            print "\nbye..."
            break
            
        print user_input
        if user_input == 'exit':
            break

        if not user_input:
            continue

        one(user_input)

if __name__ == '__main__':
    #~ optfunc.run(find)
    optfunc.main([for_ever,one])
