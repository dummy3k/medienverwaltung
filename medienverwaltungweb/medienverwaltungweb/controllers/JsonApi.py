import logging
import json
import amazonproduct

from pylons import request, response, session, tmpl_context as c, url
from pylons import config
from pylons.controllers.util import abort, redirect

from medienverwaltungweb.lib.base import BaseController, render

from medienverwaltungweb.model import meta
import medienverwaltungweb.model as model
import medienverwaltungweb.lib.amazon as amazon


log = logging.getLogger(__name__)

class JsonapiController(BaseController):

    @property
    def allow_openid(self):
        return False

    def index(self):
        return 'Hello World'

    def isbn(self):
        isbn = request.params.get('q')
        log.debug("isbn: %s" % isbn)
        if not c.user:
            self.login_user()

        retval = {'isbn':isbn, 'media': []}

        query = meta.Session\
                          .query(model.Medium)\
                          .filter(model.Medium.isbn==isbn)

        log.debug("query.count(): %s" % query.count())
        #~ if query.count() == 0:
            #~ log.debug("COUNT")
            #~ search_index = 'Books'
            #~ amazon_retval = amazon.AddMediumByISBN(isbn, search_index)
            #~ log.debug("amazon_retval: %s" % amazon_retval)

        for medium in query:
            retval['media'].append({'id':medium.id,
                                    'title':medium.title})

        ################################################################
        # amazon

        api = amazonproduct.API(config['Amazon.AccessKeyID'],
                                config['Amazon.SecretAccessKey'],
                                config['Amazon.Locale'],
                                config['Amazon.AssociateTag'])

        id_type = 'ISBN'
        search_index = 'Books'
        node = None
        try:
            node = api.item_lookup(isbn,
                                   IdType=id_type,
                                   SearchIndex=search_index,
                                    ResponseGroup="Images,ItemAttributes")

        except amazonproduct.errors.InvalidParameterValue as ex:
            log.debug("amazon InvalidParameterValue: %s" % ex)
        except Exception as ex:
            log.debug("type(ex): %s" % type(ex))
            raise

        if node:
            item = node.Items.Item
            title = unicode(item.ItemAttributes.Title)

            log.debug("title: %s" % title)
            retval['amazon_book_isbn'] = {'ASIN':str(item.ASIN),
                                          'title':title}


        return json.dumps(retval)




