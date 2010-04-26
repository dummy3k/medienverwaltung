import logging
import amazonproduct
import urllib
from StringIO import StringIO
from datetime import datetime
from pylons import config

import medienverwaltungweb.model as model
import medienverwaltungweb.lib.helpers as h
from medienverwaltungweb.model import meta
from medienverwaltungcommon.amazon import add_persons

log = logging.getLogger(__name__)

def AddMediumByISBN(isbn):
    response = {'input_isbn':isbn}
    try:
        api = amazonproduct.API(config['Amazon.AccessKeyID'],
                                config['Amazon.SecretAccessKey'])

        node = api.item_lookup(isbn,
                               IdType='ISBN',
                               SearchIndex='Books',
                                ResponseGroup="Images,ItemAttributes")
        item = node.Items.Item
        title = unicode(item.ItemAttributes.Title)
        response['title'] = title
        log.info("title: %s" % title)

        media_type = meta.Session\
                         .query(model.MediaType)\
                         .filter(model.MediaType.name == 'book')\
                         .first()

        medium = model.Medium()
        medium.title = title
        medium.created_ts = datetime.now()
        medium.updated_ts = datetime.now()
        log.debug("medium.title: %s" % medium.title)
        medium.media_type_id = media_type.id
        medium.isbn = isbn

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

        response['image_url'] = url

        meta.Session.add(medium)
        #~ session.commit()

        asin = model.MediaToAsin()
        asin.media_id = medium.id
        asin.asin = item.ASIN
        #~ session.add(asin)
        medium.asins.append(asin)

        added_persons = []
        add_persons(item, 'Author', medium, added_persons, meta.Session)
        add_persons(item, 'Creator', medium, added_persons, meta.Session)
        add_persons(item, 'Manufacturer', medium, added_persons, meta.Session)

        response['persons'] = map(lambda x: x.name, added_persons)

        meta.Session.commit()
        
        response['medium_url'] = h.url_for(controller='medium', action='edit', id=medium.id)
        response['success'] = True
        response['message'] = "Successfully added '%s'" % isbn
    except Exception, ex:
        log.error("AddMediumByISBN: %s" % ex)
        response['success'] = False
        response['message'] = str(ex)
        
    return response

    #~ medium.image_data = buffer.getvalue()

            
    #~ print unicode(msg.value, errors='replace')
    #~ print msg.value
    log.info("added: %s" % ", ".join(map(lambda x: x.name, added_persons)))
