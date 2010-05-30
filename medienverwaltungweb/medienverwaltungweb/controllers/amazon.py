import logging
import amazonproduct
import urllib
import pickle
from StringIO import StringIO
from datetime import datetime
from pprint import pprint, pformat

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config, url
from pylons.controllers.util import abort
from pylons.i18n import _, ungettext

import medienverwaltungweb.lib.helpers as h
import medienverwaltungweb.model as model
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta
from medienverwaltungcommon.amazon import add_persons, RefHelper

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

    def map_to_medium(self, id, page=1):
        """ id is media.id """
        c.item = meta.find(model.Medium, id)
        c.page = page

        query = request.params.get('query', c.item.title)
        log.debug("c.item.type: %s" % c.item.type)
        search_index = str(c.item.type.amzon_search_index)
        log.debug("search_index: %s" % search_index)

        selected_asins = request.params.get('selected_asins')
        if selected_asins:
            log.debug("selected_asin: %s" % selected_asins)
            node = self.api.item_lookup(selected_asins,
                                            ResponseGroup="Images,ItemAttributes")
            c.selected_items = node.Items.Item

        try:
            node = self.api.item_search(search_index,
                                        Title=query.encode('utf-8'),
                                        ResponseGroup="Images,ItemAttributes",
                                        ItemPage=page)
            c.items = node.Items.Item
        except Exception, ex:
            log.warn("Amzon Search error: %s" % ex)
            c.items = []

        c.query = query
        c.title = _("Amazon Search Results for '%s'" % query)
        if page > 1:
            c.title += _(", page %s") % c.page
        return render('/amazon/item_search_result.mako')

    def map_to_medium_post(self):
        media_id = request.params.get('media_id', None)

        if request.params.get('next_page', None):
            page = int(request.params.get('page', 1))
            log.debug("page: %s" % page)

            selected_asins = ','.join(h.checkboxes(request, 'item_id_'))
            log.debug("selected_asins: %s" % selected_asins)

            query = request.params.get('query')
            log.debug("query: %s" % query)

            return redirect(url(controller='amazon',
                               action='map_to_medium',
                               id=media_id,
                               page=page + 1,
                               selected_asins=selected_asins,
                               query=query))

        medium = meta.Session.query(model.Medium).get(media_id)
        asins = []
        for item in h.checkboxes(request, 'item_id_'):
            record = model.MediaToAsin()
            record.asin = item
            asins.append(item)
            medium.asins.append(record)

        h.flash(_("attached %s amazon ids to media id %s: %s")\
                % (len(asins), media_id, ", ".join(asins)))

        meta.Session.commit()
        self.__query_actors__(media_id)
        if not medium.image_data:
            return redirect(url(controller='amazon', action='query_images', id=media_id, page=None))
        else:
            return redirect(url(controller='medium', action='edit', id=media_id, page=None))

    def query_actors(self, id):
        self.__query_actors__(id)
        return redirect(url(controller='medium', action='edit', id=id))

    def __query_actors__(self, id):
        """ id = media.id """
        query = meta.Session.query(model.MediaToAsin)\
                            .filter(model.MediaToAsin.media_id==id)
        asins = map(lambda item: item.asin, query.all())
        log.debug("asins: %s" % asins)
        try:
            node = self.api.item_lookup(",".join(asins),
                                        ResponseGroup="Images,ItemAttributes")
        except Exception, ex:
            h.flash("%s: %s" % (type(ex), ex))
            return redirect(url(controller='medium', action='edit', id=id))

        added_persons = []
        medium = meta.Session.query(model.Medium).get(id)
        for item in node.Items.Item:
            log.debug("item.title: %s" % item.ItemAttributes.Title)
            log.debug("item: %s" % item.ASIN)
            add_persons(item, 'Actor', medium, added_persons, meta.Session)
            add_persons(item, 'Author', medium, added_persons, meta.Session)
            add_persons(item, 'Creator', medium, added_persons, meta.Session)
            add_persons(item, 'Director', medium, added_persons, meta.Session)
            add_persons(item, 'Manufacturer', medium, added_persons, meta.Session)

        meta.Session.commit()
        #~ if len(msg.value) > len(u"added: "):
            #~ h.flash(msg.value)

        from pylons import config
        template_name = 'person/snippets.mako'
        def_name = 'link_to_person'
        template = config['pylons.app_globals'].mako_lookup.get_template(template_name).get_def(def_name)

        if len(added_persons) > 0:
            person_list = map(lambda item: template.render_unicode(item=item, h=h), added_persons)
            person_list = ", ".join(person_list)
            h.flash(_("added persons: %s") % person_list, escape=False)
        else:
            h.flash(_("no person added"))

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
        if len(c.items) == 1:
            image_url = None
            try:
                image_url = c.items[0].LargeImage.URL
                h.flash(_("Only one image available. It was automatically choosen."))
            except:
                h.flash(_("No image available"))

            if image_url:
                self.__query_images_post__(id, str(image_url))
            return redirect(url(controller='medium', action='edit', id=id))

        c.media_id = id
        return render("amazon/image_list.mako")

    def query_images_post(self, id):
        image_url = request.params.get('url', None)
        self.__query_images_post__(id, image_url)
        return redirect(url(controller='medium', action='edit', id=id))

    def __query_images_post__(self, id, image_url):
        webFile = urllib.urlopen(image_url)
        buffer = StringIO()
        buffer.write(webFile.read())

        log.debug("id: %s" % id)
        item = meta.find(model.Medium, id)
        item.set_image_buffer(buffer)

        if item.image_data.len >= 65536:
            # 69198 defenitly fails. if the size is to blame.
            # i dont know :(
            h.flash(_("image is to big."))

            # dont do this, might be an infinite loop
            #~ return redirect_to(controller='amazon', action='query_images')
            return redirect(url(controller='medium', action='edit', id=id))

        meta.Session.add(item)
        meta.Session.commit()

    def remove_asin(self, id):
        asin_str = request.params.get('asin', None)
        asin = meta.Session.query(model.MediaToAsin)\
                           .filter(model.MediaToAsin.asin==asin_str)\
                           .first()

        meta.Session.delete(asin)
        meta.Session.commit()
        return redirect(url(controller='medium', action='edit', id=id))

    def clear_persons(self, id):
        item = meta.find(model.Medium, id)
        cnt = 0
        for person2media in item.persons_to_media:
            meta.Session.delete(person2media)
            cnt += 1

        meta.Session.commit()
        h.flash(ungettext("removed %d person", "removed %d persons", cnt) % cnt)
        return redirect(url(controller='medium', action='edit', id=id))


