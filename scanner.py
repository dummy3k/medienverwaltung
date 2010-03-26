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

def one(isbn):
    print "ISBN: %s" % isbn
    node = api.item_lookup(isbn, IdType='ISBN', SearchIndex=SearchIndex)
    item = node.Items.Item
    #~ h.ipython()()
    title = unicode(item.ItemAttributes.Title)
    #~ title = item.ItemAttributes.Title
    print title

    record = model.Medium()
    record.title = title
    record.media_type_id = 2
    
    engine = create_engine(config.get('sqlalchemy', 'url'))
    session = scoped_session(sessionmaker())
    session.configure(bind=engine)
    session.add(record)
    session.commit()
    #~ model.meta.Session.add(record)
    #~ model.meta.Session.commit()

def for_ever():
    while True:
        user_input = raw_input("ISBN:")
        print user_input
        if user_input == 'exit':
            break

        if not user_input:
            continue
        
        node = api.item_lookup(user_input, IdType='ISBN', SearchIndex=SearchIndex)
        item = node.Items.Item
        #~ h.ipython()()
        print unicode(item.ItemAttributes.Title)

if __name__ == '__main__':
    #~ optfunc.run(find)
    optfunc.main([for_ever,one])
