import logging
import amazonproduct
import urllib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons import config
from pylons.controllers.util import abort

from medienverwaltungweb.lib.base import BaseController, render
import medienverwaltungweb.lib.helpers as h
from medienverwaltungweb.model import meta
import medienverwaltungweb.model as model

log = logging.getLogger(__name__)

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

        SearchIndex = 'DVD'
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
        node = self.api.item_search(self.SearchIndex,
                                    Title=c.item.title.encode('utf-8'),
                                    ResponseGroup="Images,ItemAttributes")
        c.items = node.Items.Item
        return render('/amazon/item_search_result.mako')


    def map_to_medium_post(self):
        media_id = request.params.get('media_id', None)
        for item in h.checkboxes(request, 'item_id_'):
            record = model.MediaToAsin()
            record.media_id = media_id
            record.asin = item
            meta.Session.add(record)
            h.flash("attached %s to %s" % (item, media_id))


        meta.Session.commit()

        #query = meta.Session.query(model.Person)
        #actor = query.filter(model.RelationType.name=='Actor').first()
        #if not actor_relation:
            #abort(404)
        #log.debug("actor: %s" % actor_relation)

        #for item in h.checkboxes(request, 'item_id_'):
            ##~ log.debug("item: %s" % item)
            ##~ db_item = meta.find(model.Medium, item)
            ##~ meta.Session.delete(db_item)

        return redirect_to(controller='medium', action='edit')


    def query_actors(self, id):
        """ id = media.id """
        query = meta.Session.query(model.MediaToAsin)
        asins = query.filter(model.MediaToAsin.media_id==id).all()
        log.debug("asins: %s" % asins)

        query = meta.Session.query(model.RelationType)
        actor_relation = query.filter(model.RelationType.name=='Actor').first()
        if not actor_relation:
            abort(404)
        log.debug("actor_relation: %s" % actor_relation)

        for item in asins:
            node = self.api.item_lookup(item.asin,
                                        ResponseGroup="Images,ItemAttributes")
            item = node.Items.Item[0]
            log.debug("item.title: %s" % item.ItemAttributes.Title)
            if 'Actor' in dir(item.ItemAttributes):
                for subitem in item.ItemAttributes.Actor:
                    log.debug("Actor: %s" % subitem)
                    query = meta.Session.query(model.Person)
                    actor = query.filter(model.Person.name==str(subitem)).first()
                    if not actor:
                        log.info("new actor: %s" % str(subitem))
                        actor = model.Person()
                        actor.name = str(subitem)
                        meta.Session.save(actor)
                        meta.Session.commit()
                        h.flash("added: %s" % actor)


                    record = model.PersonToMedia()
                    record.person_id = actor.id
                    record.medium_id = id
                    record.type_id = actor_relation.id
                    meta.Session.save(record)
                    h.flash("added2: %s" % record)


            else:
                log.warn("asin %s has now actors" % item.ASIN)

            log.debug("item: %s" % item.ASIN)

        meta.Session.commit()
        return redirect_to(controller='medium', action='edit')

