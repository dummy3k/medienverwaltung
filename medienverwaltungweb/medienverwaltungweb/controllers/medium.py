import logging
import Image, ImageFile
from StringIO import StringIO

from sqlalchemy.sql import select, join, and_, or_, not_
from webhelpers import paginate
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import medienverwaltungweb.model as model
import medienverwaltungweb.lib.helpers as h
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta

log = logging.getLogger(__name__)

class MediumController(BaseController):
    def index(self, id=None):
        if id:
            return self.edit(id)
        else:
            return self.list()

    def mass_add(self):
        c.types = meta.Session.query(model.MediaType).all()
        return render('medium/mass_add.mako')

    def mass_add_post(self):
        if not request.params.get('title'):
            h.flash("please specify name")
            return redirect_to(action='mass_add')

        count = 0
        for item in request.params.get('title').split('\n'):
            query = meta.Session\
                .query(model.Medium)\
                .filter(model.Medium.title==item)
            if query.first() != None:
                h.flash("medium elready exists: %s" % query.first())
                continue
                
            record = model.Medium()
            record.title = item
            record.media_type_id = request.params.get('media_type')
            meta.Session.save(record)
            count += 1
        meta.Session.commit()

        h.flash("added: %s media" % count)
        return redirect_to(action='index')

    def list(self, type=None, page=1, tag=None):
        self.__prepare_list__(type, page, tag)
        c.title = "All Media"
        c.pager_action = "list"
        return render('medium/list.mako')

    def list_gallery(self, type=None, page=1, tag=None):
        self.__prepare_list__(type, page, tag)
        c.next_link = h.url_for(controller='medium', action='list_gallery', page=int(page)+1)
        c.prev_link = h.url_for(controller='medium', action='list_gallery', page=int(page)-1)
        return render('medium/list_gallery.mako')
    
    def __prepare_list__(self, type=None, page=1, tag=None):
        log.debug("type: %s" % type)
        query = meta.Session.query(model.Medium)
        
        if type:
            if type[-1:] == 's':
                type = type[:-1]
                
            query = query.join(model.MediaType)\
                         .filter(model.MediaType.name==type)

        log.debug("tag: %s" % tag)
        if tag:
            query = query.join(model.Tag)\
                         .filter(model.Tag.name==tag)

        c.items = query.all()
        c.page = paginate.Page(query, page)

        if not type:
            tag_query = select([model.tags_table.c.name]).distinct()
        else:
            tag_query = select([model.tags_table.c.name], from_obj=[
                model.tags_table.join(model.media_table)\
                                .join(model.media_types_table)
            ]).where(model.media_types_table.c.name==type)\
              .distinct()

        tag_query.bind = meta.engine
        c.tags = map(lambda x: x[0], tag_query.execute())

    def list_no_image(self, page=1):
        query = meta.Session\
            .query(model.Medium)\
            .filter(model.Medium.image_data == None)
        query = query.order_by(model.Medium.id.desc())
        c.items = query.all()
        c.page = paginate.Page(query, page)
        c.title = "Media without images"
        c.pager_action = "list_no_image"
        return render('medium/list.mako')

    def delete(self):
        msg = ""
        for item in h.checkboxes(request, 'item_id_'):
            db_item = meta.find(model.Medium, item)
            meta.Session.delete(db_item)
            h.flash("deleted: %s" % db_item)

        meta.Session.commit()

        return redirect_to(action='index')

    def delete_one(self, id):
        msg = ""
        db_item = meta.find(model.Medium, id)
        meta.Session.delete(db_item)
        h.flash("deleted: %s" % db_item)

        meta.Session.commit()

        return redirect_to(action='index')

    def edit(self, id):
        log.debug("id: %s" % id)
        c.item = meta.find(model.Medium, id)
        c.persons = {}

        query = meta.Session.query(model.MediaToAsin)
        result = query.filter(model.MediaToAsin.media_id==id).all()
        c.asins = []
        for item in result:
            c.asins.append(item.asin)

        log.debug("!!!!!!!!")
        #~ query = meta.Session\
            #~ .query(model.Person)\
            #~ .join(model.PersonToMedia)\
            #~ .join(model.RelationType)\
            #~ .filter(model.PersonToMedia.medium_id==id)\
            #~ .all()
        query = meta.Session\
            .query(model.PersonToMedia)\
            .filter(model.PersonToMedia.medium_id==id)\
            .all()
        for item in query:
            log.debug("Person2: %s" % item.person)

            #~ sub_query = meta.Session.query(model.RelationType)
            #~ actor_relation = sub_query.filter(model.RelationType.name=='Actor').first()
            #~ if not actor_relation:
                #~ abort(404)
            #~ log.debug("actor_relation: %s" % actor_relation)

            if item.relation.name in c.persons:
                c.persons[item.relation.name].append(item.person)
            else:
                c.persons[item.relation.name] = [item.person]

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
        item.set_tagstring(request.params.get('tags'))
        meta.Session.update(item)
        meta.Session.commit()
        h.flash("updated: %s" % item)
        return redirect_to(action='edit', id=id)

    def image(self, id, width, height):
        item = meta.find(model.Medium, id)

        p = ImageFile.Parser()
        p.feed(item.image_data.getvalue())
        #~ p.feed(StringIO(item.image_data.getvalue()))
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

    def next_without_image(self, id):
        query = meta.Session\
            .query(model.Medium)\
            .filter(model.Medium.image_data == None)\
            .filter(model.Medium.id < id)\
            .order_by(model.Medium.id.desc())

        medium = query.first()
        if not medium:
            h.flash("all media after this have a image")
            return redirect_to(action='edit', id=id)
            
        return redirect_to(action='edit', id=medium.id)
        
