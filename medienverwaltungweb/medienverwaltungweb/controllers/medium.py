import logging
import Image, ImageFile
from StringIO import StringIO

from sqlalchemy.sql import select, and_, or_, not_
from webhelpers import paginate
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import medienverwaltungweb.model as model
import medienverwaltungweb.lib.helpers as h
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta

log = logging.getLogger(__name__)

class MediumController(BaseController):
    def index(self):
        return self.list()

    def mass_add(self):
        return render('medium/mass_add.mako')

    def mass_add_post(self):
        if not request.params.get('title'):
            h.flash("please specify name")
            return redirect_to(action='mass_add')

        count = 0
        for item in request.params.get('title').split('\n'):
            record = model.Medium()
            record.title = item
            meta.Session.save(record)
            count += 1
        meta.Session.commit()

        h.flash("added: %s media" % count)
        return redirect_to(action='index')

    def list(self, page=1):
        query = meta.Session.query(model.Medium)
        c.items = query.all()
        c.page = paginate.Page(query, page)
        return render('medium/list.mako')

    def list_gallery(self, page=1):
        query = meta.Session\
            .query(model.Medium)\
            .filter(model.Medium.image_data != None)
            
        c.items = query.all()
        c.page = paginate.Page(query, page)
        return render('medium/list_gallery.mako')

    def delete(self):
        msg = ""
        #~ for item in request.params:
            #~ if item.startswith('item_id'):
                #~ id = request.params[item]
                #~ db_item = meta.find(model.Medium, id)
                #~ meta.Session.delete(db_item)
                #~ h.flash("deleted: %s" % db_item)

        for item in h.checkboxes(request, 'item_id_'):
            db_item = meta.find(model.Medium, item)
            meta.Session.delete(db_item)
            h.flash("deleted: %s" % db_item)

        meta.Session.commit()

        return redirect_to(action='index')

    def edit(self, id):
        log.debug("id: %s" % id)
        c.item = meta.find(model.Medium, id)
        c.persons = {'Actor':[]}

        query = meta.Session.query(model.MediaToAsin)
        result = query.filter(model.MediaToAsin.media_id==id).all()
        c.asins = []
        for item in result:
            c.asins.append(item.asin)

        query = meta.Session.query(model.RelationType)
        actor_relation = query.filter(model.RelationType.name=='Actor').first()
        if not actor_relation:
            abort(404)
        log.debug("actor_relation: %s" % actor_relation)

        query = meta.Session\
            .query(model.Person)\
            .join(model.PersonToMedia)\
            .filter(model.PersonToMedia.medium_id==id)\
            .all()
        for item in query:
            log.debug("Person: %s" % item)
            c.persons['Actor'].append(item)

        #~ query
        #~ query.join(model.PersonToMedia)

        #~ persons = select([persons,
        #~ for item in persons:
            #~ log.debug("!!!person: %s" % item)

        return render('medium/edit.mako')

    def edit_post(self):
        id = request.params.get('id')
        item = meta.find(model.Medium, id)
        item.title = request.params.get('title')
        item.image_url = request.params.get('image_url')
        meta.Session.update(item)
        meta.Session.commit()
        h.flash("updated: %s" % item)
        return redirect_to(action='index')


    def foo(self):
        return "Hello World!"
    def image(self, id, width, height):
        item = meta.find(model.Medium, id)
        #~ log.debug(item.image_data.)

        #~ mode = 'RGB'
        #~ img = Image.frombuffer(mode, (100, 100), item.image_data.getvalue())
        #~ log.debug("mode: %s" % mode)

        p = ImageFile.Parser()
        p.feed(item.image_data.getvalue())
        img = p.close()

        log.debug("size: %s, %s" % (width, height))
        size = int(width), int(height)
        img.thumbnail(size)
        log.debug("imgsize: %s, %s" % img.size)

        buffer = StringIO()
        img.save(buffer, format='png')
        response.content_type = 'image/png'
        return buffer.getvalue()

        # set the response type to PNG, since we at least hope to return a PNG image here
        #~ return item.image_data.getvalue()
        #~ return img.tostring()
