import logging
import amazonproduct
import urllib
from StringIO import StringIO

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons import config
from pylons.controllers.util import abort

from medienverwaltungweb.lib.base import BaseController, render
import medienverwaltungweb.lib.helpers as h
from medienverwaltungweb.model import meta
import medienverwaltungweb.model as model
from medienverwaltungcommon.amazon import add_persons
log = logging.getLogger(__name__)

class RefHelper():
    def __init__(self, value):
        self.value = value
        
class AmazonController(BaseController):
    def __init__(self):
        BaseController.__init__(self)
        self.api = amazonproduct.API(config['Amazon.AccessKeyID'],
                                     config['Amazon.SecretAccessKey'])
        self.SearchIndex = 'DVD'

    def index(self):
        return render('/amazon/add_these.mako')

    def add_one_post(self):
        add_this = request.params.get('add_this', None)

        #~ SearchIndex = 'DVD'
        log.debug("add_this: %s" % add_this)
        node = self.api.item_search(SearchIndex,
                                    Title=add_this.encode('utf-8'),
                                    ResponseGroup="Images,ItemAttributes")
        c.items = node.Items.Item
        c.query = add_this
        return render('/amazon/item_search_result.mako')

    def show_asin(self, id):
        node = self.api.item_lookup(id,
                                    ResponseGroup="Images,ItemAttributes")
        c.item = node.Items.Item[0]
        return render('/amazon/item_lookup_result.mako')

    def map_to_medium(self, id):
        """ id is media.id """
        c.item = meta.find(model.Medium, id)

        query  = request.params.get('query', c.item.title)
        log.debug("c.item.type: %s" % c.item.type)
        search_index = c.item.type.amzon_search_index
        log.debug("search_index: %s" % search_index)
        try:
            node = self.api.item_search(search_index,
                                        Title=query.encode('utf-8'),
                                        ResponseGroup="Images,ItemAttributes")
            c.items = node.Items.Item
        except:
            c.items = []
            
        c.query = query
        return render('/amazon/item_search_result.mako')

    def map_to_medium_post(self):
        media_id = request.params.get('media_id', None)
        asins = []
        for item in h.checkboxes(request, 'item_id_'):
            record = model.MediaToAsin()
            record.media_id = media_id
            record.asin = item
            meta.Session.add(record)
            asins.append(item)
            
        h.flash("attached %s amazon ids to media id %s: %s"\
                % (len(asins), media_id, ", ".join(asins)))
                   
        meta.Session.commit()
        return redirect_to(controller='medium', action='edit')

    def query_actors(self, id):
        """ id = media.id """
        query = meta.Session.query(model.MediaToAsin)\
                            .filter(model.MediaToAsin.media_id==id)
        asins = map(lambda item: item.asin, query.all())
        msg = RefHelper(u"added: ")
        
        node = self.api.item_lookup(",".join(asins),
                                    ResponseGroup="Images,ItemAttributes")
        for item in node.Items.Item:
            log.debug("item.title: %s" % item.ItemAttributes.Title)
            log.debug("item: %s" % item.ASIN)
            add_persons(item, 'Actor', id, msg, meta.Session)
            add_persons(item, 'Creator', id, msg, meta.Session)
            add_persons(item, 'Director', id, msg, meta.Session)
            add_persons(item, 'Manufacturer', id, msg, meta.Session)

        meta.Session.commit()
        if len(msg.value) > len(u"added: "):
            h.flash(msg.value)
        return redirect_to(controller='medium', action='edit')
        
    def query_images(self, id):
        """ show the user a selection of available images """

        query = meta.Session.query(model.MediaToAsin)\
                            .filter(model.MediaToAsin.media_id==id)

        c.items = []
        asins = map(lambda item: item.asin, query.all())
        if len(asins) > 10:
            log.warn("number of asins is greater 10")
        node = self.api.item_lookup(",".join(asins),
                                    ResponseGroup="Images")
        c.items = node.Items.Item
        return render("amazon/image_list.mako")
        
    def query_images_post(self, id):
        url = request.params.get('url', None)
        webFile = urllib.urlopen(url)
        buffer = StringIO()
        buffer.write(webFile.read())

        item = meta.find(model.Medium, id)
        item.image_data = buffer
        meta.Session.update(item)
        meta.Session.commit()
        
        return redirect_to(controller='medium', action='edit')
