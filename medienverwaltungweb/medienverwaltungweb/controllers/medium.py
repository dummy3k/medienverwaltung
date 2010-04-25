import logging
import Image, ImageFile
from StringIO import StringIO
from datetime import datetime
from pprint import pprint, pformat

from sqlalchemy import func
from sqlalchemy.sql import select, join, and_, or_, not_
from webhelpers import paginate
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, etag_cache
from pylons.i18n import _, ungettext
from mako.template import Template

import medienverwaltungweb.lib.helpers as h
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta
import medienverwaltungweb.model as model

log = logging.getLogger(__name__)

# names for babel to pick up:
_('Author')
_('Actor')
_('Director')
_('Manufacturer')
_('Creator')
_('Book')
_('Dvd')
_('Created_ts')
_('Updated_ts')

anchor_tmpl = Template("<a href='${url}'>${text|h}</a>")

class MediumController(BaseController):
    def index(self, id=None, type=None, page=1, tag=None):
        if id:
            return self.edit(id)
        else:
            return self.list(type, page, tag)

    def mass_add(self):
        c.types = meta.Session.query(model.MediaType).all()
        return render('medium/mass_add.mako')

    def mass_add_post(self):
        if not request.params.get('title'):
            h.flash(_("please specify name"))
            return redirect_to(action='mass_add')

        if int(request.params.get('media_type', -1)) < 0:
            h.flash(_("please specify media type"))
            return redirect_to(action='mass_add')

        count = 0
        new_media = []
        for item in request.params.get('title').split('\n'):
            if not item.strip():
                continue

            query = meta.Session\
                .query(model.Medium)\
                .filter(model.Medium.title==item)
            if query.first() != None:
                first_item = query.first()
                h.flash(_("medium elready exists: %s") %\
                    anchor_tmpl.render(url=h.url_for(action='edit', id=first_item.id),
                                       text=h.html_escape(first_item.title)), escape=False)
                continue

            record = model.Medium()
            record.title = item.strip()
            record.created_ts = datetime.now()
            record.updated_ts = datetime.now()
            record.media_type_id = request.params.get('media_type')
            meta.Session.add(record)
            count += 1
            new_media.append(record)

        if len(new_media) > 0:
            meta.Session.commit()
            log.debug("new_media: %s" % unicode(new_media[0].title))
            log.debug("type new_media: %s" % type(new_media[0].title))
            link_list = map(lambda x: anchor_tmpl.render_unicode(url=h.url_for(action='edit', id=x.id), text=x.title), new_media)
            link_list = ", ".join(link_list)
            msg = ungettext("added medium %(media)s",
                            "added %(num)d media: %(media)s",
                            len(new_media)) % {'num':len(new_media),
                                               'media':link_list}
            h.flash(msg, escape=False)
            #~ h.flash(UnsafeString(msg))

        if len(new_media) == 1:
            return redirect_to(action='edit', id=new_media[0].id)
        else:
            return redirect_to(action='index')

    def list(self, type=None, page=1, tag=None):
        if type == 'books':
            c.title = _("Books List")
        elif type == 'dvds':
            c.title = _("DVDs List")
        elif type:
            c.title = _("List of unknown type '%s'") % type
        else:
            c.title = _("All Media List")

        self.__prepare_list__(False, type, page, tag)

        c.pager_action = "list"
        c.return_to = h.url_for(order=c.order)
        return render('medium/list.mako')

    def list_gallery(self, type=None, page=1, tag=None):
        if type == 'books':
            c.title = _("Books Gallery")
        elif type == 'dvds':
            c.title = _("DVDs Gallery")
        elif type:
            c.title = _("Gallery of unknown type '%s'") % type
        else:
            c.title = _("All Media Gallery")

        self.__prepare_list__(True, type, page, tag)

        c.pager_action = "list_gallery"
        return render('medium/list_gallery.mako')

    def __get_tags__(self, tag_name, media_type_name):
        """ get all tags from all media.
            If tag_name is specified only media tagged with this is
            considered.
            If media_type_name is specified only media by this type
            is considered.
            Returns a tuple (tag_name, count) for each tag.
        """
        join_clause = model.tags_table.join(model.media_table)

        if tag_name:
            sub_tags_table = model.tags_table.alias('sub_tags')
            join_clause = join_clause.join(sub_tags_table)

        if media_type_name:
            sub_media_types_table = model.media_types_table.alias('sub_media_types_table')
            join_clause = join_clause.join(sub_media_types_table)

        tag_query = select([model.tags_table.c.name],
                           from_obj=[join_clause])

        if tag_name:
            tag_query = tag_query.where(sub_tags_table.c.name==tag_name)
            tag_query = tag_query.where(model.tags_table.c.name != tag_name)

        if media_type_name:
            tag_query = tag_query.where(sub_media_types_table.c.name==media_type_name)
            log.debug("tag_query: %s" % tag_query)

        #~ tag_query = tag_query.group_by(model.tags_table.c.name)\
                             #~ .order_by(cnt_col.desc())

        cnt_col = func.count()
        query = select([model.tags_table.c.name, cnt_col],
                       from_obj=[model.tags_table])
        query = query.where(model.tags_table.c.name.in_(tag_query))
        query = query.group_by(model.tags_table.c.name)
        query = query.order_by(cnt_col.desc())
        query.bind = meta.engine

        retval = map(lambda x: (x[0], x[1]), query.execute())
        return retval

    def __prepare_list__(self, with_images, type=None, page=1, tag=None,
                         no_images=False):
        if tag:
            c.title += _(", tagged %s") % tag.capitalize()

        if type and type[-1:] == 's':
            type = type[:-1]

        log.debug("type: %s" % type)
        c.tags = self.__get_tags__(tag, type)
        log.debug("c.tags: %s" % len(c.tags))

        query = meta.Session.query(model.Medium)

        if type:
            query = query.join(model.MediaType)\
                         .filter(model.MediaType.name==type)

        log.debug("tag: %s" % tag)
        if tag:
            query = query.join(model.Tag)\
                         .filter(model.Tag.name==tag)

        if with_images:
            c.without_images_cnt = query.filter(model.Medium.image_data==None).count()
            if c.without_images_cnt > 0 and c.without_images_cnt < 5:
                c.without_images = query.filter(model.Medium.image_data==None)

            query = query.filter(model.Medium.image_data!=None)

        elif no_images:
            query = query.filter(model.Medium.image_data==None)

        c.order = request.params.get('order')
        if not c.order:
            query = query.order_by(model.Medium.title)
        elif c.order.endswith('_desc'):
            sort_name = c.order[:-5]
            query = query.order_by(model.Medium.__dict__[sort_name].desc())
            c.title += _(", sorted by %s descending") % _(sort_name.capitalize())
            log.debug("c.order: '%s'" % sort_name.capitalize())
        else:
            query = query.order_by(model.Medium.__dict__[c.order])
            c.title += _(", sorted by %s") % _(c.order.capitalize())

        log.debug("c.items: %s" % len(c.items))
        if not 'items_per_page' in session:
            items_per_page = 14
        else:
            items_per_page = session['items_per_page']

        c.page = paginate.Page(query, page, items_per_page=items_per_page)
        c.page_args = {'controller':'medium',
                       'action':'list',
                       'order':c.order}

        if int(page) > 1:
            c.title += _(", page %s") % c.page.page


    def list_no_image(self, page=1, type=None, tag=None):
        #~ query = meta.Session\
            #~ .query(model.Medium)\
            #~ .filter(model.Medium.image_data == None)
        #~ query = query.order_by(model.Medium.id.desc())
        #~ c.items = query.all()
        #~ c.page = paginate.Page(query, page)

        self.__prepare_list__(False, type, page, tag, no_images=True)

        c.title = _("Media without images")
        c.pager_action = "list_no_image"
        return render('medium/list.mako')

    def delete(self):
        for item in h.checkboxes(request, 'item_id_'):
            db_item = meta.find(model.Medium, item)
            meta.Session.delete(db_item)
            h.flash(_("deleted: %s") % db_item.title)

        meta.Session.commit()

        return redirect_to(action='index')

    def delete_one(self, id):
        log.debug("delete_one(%s)" % id)
        db_item = meta.find(model.Medium, id)
        meta.Session.delete(db_item)
        meta.Session.commit()
        h.flash(_("deleted: %s") % db_item.title)
        if request.params.get('return_to'):
            return redirect_to(str(request.params.get('return_to')))
        else:
            return redirect_to(action='index', id=None)

    def edit(self, id):
        log.debug("id: %s" % id)
        c.item = meta.find(model.Medium, id)
        c.persons = {}

        query = meta.Session.query(model.MediaToAsin)
        result = query.filter(model.MediaToAsin.media_id==id).all()
        c.asins = []
        for item in result:
            c.asins.append(item.asin)

        query = meta.Session\
            .query(model.PersonToMedia)\
            .filter(model.PersonToMedia.medium_id==id)\
            .all()
        for item in query:
            log.debug("Person2: %s" % item.person)

            if item.relation.name in c.persons:
                c.persons[item.relation.name].append(item)
            else:
                c.persons[item.relation.name] = [item]

        c.borrowed_by = meta.Session.query(model.Borrower)\
                                    .join(model.BorrowAct)\
                                    .filter(model.BorrowAct.media_id == id)\
                                    .filter(model.BorrowAct.returned_ts == None)\
                                    .first()

        # All Tag Names for this medium
        query1 = select([model.tags_table.c.name])
        query1 = query1.where(model.tags_table.c.media_id == id)

        cnt_col = func.count()
        query = select([model.tags_table.c.name, cnt_col],
                       from_obj=[model.tags_table])
        query = query.where(model.tags_table.c.name.in_(query1))
        query = query.group_by(model.tags_table.c.name)
        query = query.order_by(cnt_col.desc())
        query.bind = meta.engine
        c.tags = map(lambda x: (x[0], x[1]), query.execute())

        return render('medium/edit.mako')

    def edit_post(self):
        id = request.params.get('id')
        item = meta.find(model.Medium, id)
        item.title = request.params.get('title')
        item.image_url = request.params.get('image_url')
        item.updated_ts = datetime.now()
        item.set_tagstring(request.params.get('tags'))
        meta.Session.update(item)
        meta.Session.commit()
        h.flash(_("updated: '%s'") % h.html_escape(item.title))

        return_to = request.params.get('return_to')
        log.debug("return_to: %s" % return_to)
        if return_to:
            return redirect_to(str(return_to))
        else:
            #~ return redirect_to()
            return redirect_to(action='edit', id=id)

        #~ return redirect_to(action='edit', id=id)

    def image(self, id, width, height):
        item = meta.find(model.Medium, id)
        etag_cache(str(item.updated_ts))

        p = ImageFile.Parser()
        p.feed(item.image_data.getvalue())
        img = p.close()

        if item.image_crop:
            img = img.crop(item.image_crop)

        #~ log.debug("size: %s, %s" % (width, height))
        size = int(width), int(height)
        img.thumbnail(size)
        #~ log.debug("imgsize: %s, %s" % img.size)

        buffer = StringIO()
        img.save(buffer, format='png')
        response.content_type = 'image/png'

        return buffer.getvalue()

    def raw_image(self, id):
        item = meta.find(model.Medium, id)

        p = ImageFile.Parser()
        p.feed(item.image_data.getvalue())
        img = p.close()

        buffer = StringIO()
        img.save(buffer, format='png')
        response.content_type = 'image/png'

        etag_cache(str(item.updated_ts))
        return buffer.getvalue()

    def next_without_image(self, id):
        query = meta.Session\
            .query(model.Medium)\
            .filter(model.Medium.image_data == None)\
            .filter(model.Medium.id < id)\
            .order_by(model.Medium.id.desc())

        medium = query.first()
        if not medium:
            h.flash(_("all media after this have an image"))
            return redirect_to(action='edit', id=id)

        return redirect_to(action='edit', id=medium.id, return_to=request.params.get('return_to'))
    def crop_image(self, id):
        c.item = meta.find(model.Medium, id)
        return render('medium/crop_image.mako')

    def crop_image_post(self, id):
        crop = (int(request.params.get('x')),
                int(request.params.get('y')),
                int(request.params.get('x2')),
                int(request.params.get('y2')))

        item = meta.find(model.Medium, id)
        item.image_crop = crop
        item.updated_ts = datetime.now()
        meta.Session.update(item)
        meta.Session.commit()
        h.flash(_("updated: '%s'") % h.html_escape(item.title))

        return_to = request.params.get('return_to')
        log.debug("return_to: %s" % return_to)
        if return_to:
            return redirect_to(str(return_to))
        else:
            return redirect_to(action='edit', id=id)

    def debug(self):
        log.debug("START DEBUG")
        #~ h.flash(u"testing \xc3\xa4")
        h.flash("<i>blah</i>", False)
        return redirect_to(action='index')
    def set_view_options(self, type=None, tag=None):
        items_per_page = request.params.get('items_per_page')
        if not items_per_page or int(items_per_page) <= 0:
            h.flash(_("'Number of images' must be greater then null"))
            return redirect_to(action='list_gallery', type=type, tag=tag)

        items_per_page = int(items_per_page)
        h.flash(_("%d images will be display for now on") % items_per_page)
        session['items_per_page'] = items_per_page
        session.save()

        #~ h.flash("session, items_per_page: %s" % session['items_per_page'])
        return redirect_to(action='list_gallery', type=type, tag=tag)
