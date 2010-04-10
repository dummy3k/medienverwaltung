if __name__ == '__main__':
    import logging.config
    logging.config.fileConfig("settings.conf")

import amazonproduct
import ConfigParser
from optfunc import optfunc
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import urllib
from StringIO import StringIO
import logging
import os
from datetime import datetime

import helper as h
import medienverwaltungweb.model as model
from medienverwaltungcommon.amazon import add_persons, RefHelper

log = logging.getLogger(__name__)
isbn_log = logging.getLogger('isbn')

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
    isbn_log.info("ISBN: %s" % isbn)
    node = api.item_lookup(isbn,
                           IdType='ISBN',
                           SearchIndex=SearchIndex,
                            ResponseGroup="Images,ItemAttributes")
    item = node.Items.Item
    title = unicode(item.ItemAttributes.Title)
    #~ title = item.ItemAttributes.Title
    #~ h.ipython()()
    #~ print title
    log.info("title: %s" % title)

    media_type = session.query(model.MediaType)\
                        .filter(model.MediaType.name == 'book')\
                        .first()

    medium = model.Medium()
    medium.title = title
    medium.created_ts = datetime.now()
    medium.updated_ts = datetime.now()
    log.debug("medium.title: %s" % medium.title)
    medium.media_type_id = media_type.id
    medium.isbn = isbn
    #~ medium.image_data = buffer.getvalue()

    try:
        url = str(item.LargeImage.URL)
    except:
        url = None
        log.warn("%s has no image" % medium)
        
    if url:
        print url
        webFile = urllib.urlopen(url)
        buffer = StringIO()
        buffer.write(webFile.read())
        if buffer.len > 65536:
            log.warn("image is too big")
        else:
            medium.image_data = buffer
            
    session.add(medium)
    session.commit()

    asin = model.MediaToAsin()
    asin.media_id = medium.id
    asin.asin = item.ASIN
    #~ session.add(asin)
    medium.asins.append(asin)

    # Languages
    msg = RefHelper(u"added: ")
    add_persons(item, 'Author', medium.id, msg, session)
    add_persons(item, 'Creator', medium.id, msg, session)
    add_persons(item, 'Manufacturer', medium.id, msg, session)

    session.commit()
    #~ print unicode(msg.value, errors='replace')
    print msg.value
    

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

        try:
            one(user_input)
            os.system('play -q audio/success.wav')
        except:
            os.system('play -q audio/failure.wav')

if __name__ == '__main__':
    #~ optfunc.run(find)
    optfunc.main([for_ever,one])
