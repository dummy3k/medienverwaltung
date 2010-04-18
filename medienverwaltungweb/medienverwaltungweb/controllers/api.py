import logging
import amazonproduct
from datetime import datetime
import urllib
from StringIO import StringIO

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.controllers import XMLRPCController
from pylons import config

from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta
import medienverwaltungweb.model as model
from medienverwaltungcommon.amazon import add_persons
import medienverwaltungweb.lib.helpers as h

log = logging.getLogger(__name__)

class ApiController(XMLRPCController):
    def index(self):
        return "API Interface"
        
    def sayhello(self, s):
        return 'Hello %s' % s

    sayhello.signature = [ ['struct', 'string'] ]


    def AddMediumByISBN(self, isbn):
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
            response['success'] = False
            response['message'] = str(ex)
            
        return response

        #~ medium.image_data = buffer.getvalue()

                
        #~ print unicode(msg.value, errors='replace')
        #~ print msg.value
        print "added: %s" % ", ".join(map(lambda x: x.name, added_persons))

    AddMediumByISBN.signature = [ ['struct', 'string'] ]
