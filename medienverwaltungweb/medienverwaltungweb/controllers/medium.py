# -*- coding: utf-8 -*-

import logging
import Image, ImageFile #remove me
import re
from StringIO import StringIO  #remove me
from datetime import datetime
from pprint import pprint, pformat

import PyRSS2Gen
from sqlalchemy import func
from sqlalchemy.sql import select, join, and_, or_, not_
from webhelpers import paginate
from pylons import request, response, session, tmpl_context as c
from pylons import config, url
from pylons.controllers.util import abort, redirect, etag_cache
from pylons.i18n import _, ungettext
from mako.template import Template
from mako.filters import html_escape

import medienverwaltungweb.lib.helpers as h
import medienverwaltungweb.model as model
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta

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
            return redirect(url(controller='medium', action='mass_add'))

        if int(request.params.get('media_type', -1)) < 0:
            h.flash(_("please specify media type"))
            return self.mass_add()

        media_type_obj = meta.Session.query(model.MediaType).get(request.params.get('media_type', -1))
        
        
        count = 0
        new_media = []
        failed = []
        for item in request.params.get('title').split('\n'):
            if not item.strip():
                continue

            query = meta.Session\
                .query(model.Medium)\
                .filter(or_(model.Medium.title==item,
                            model.Medium.isbn==item))
            if query.first() != None:
                first_item = query.first()
                h.flash(_("medium already exists: %s") %\
                    anchor_tmpl.render_unicode(url=h.url_for(controller='medium', action='edit', id=first_item.id),
                                       text=h.html_escape(first_item.title)), escape=False)
                continue

            log.debug("!!!item: %s" % item)
            if re.match('^\d+\s*$', item):
                #~ log.info("@@@@@@@@@@@@@@@@@@ treat input as isbn: %s" % item)
                import medienverwaltungweb.lib.amazon as amazon
                result = amazon.AddMediumByISBN(item, media_type_obj.amzon_search_index)
                if not result:
                    #~ h.flash(_("I tried to use '%s' as an isbn, but amazon didn't find it.") % item)
                    h.flash(_("Amzon does not knwo what '%s' is.") % item)
                    failed.append(item)
                    continue

                elif not result['success']:
                    h.flash(_("Amazon Lookup failed with the following error: %s") % result['message'])
                    failed.append(item)
                    continue

                medium_id = result['medium_id']
                record = meta.Session.query(model.Medium).get(medium_id)
                new_media.append(record)
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
            link_list = map(lambda x: anchor_tmpl.render_unicode(url=h.url_for(controller='medium', action='edit', id=x.id), text=x.title), new_media)
            link_list = ", ".join(link_list)
            msg = ungettext("added medium %(media)s",
                            "added %(num)d media: %(media)s",
                            len(new_media)) % {'num':len(new_media),
                                               'media':link_list}
            h.flash(msg, escape=False)
            #~ h.flash(UnsafeString(msg))

        if len(new_media) == 1:
            return redirect(url(controller='medium', action='edit', id=new_media[0].id))
        else:
            return redirect(url(controller='medium', action='index'))

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
        c.return_to = h.url_for(controller='medium', action='list', order=c.order)

        c.rss_feeds = [{'title':_("New Media"),
                        'link':h.url_for(controller='medium', action='new_media_rss')},
                       {'title':_("Updated Media"),
                        'link':h.url_for(controller='medium', action='updated_media_rss')}]
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
        c.rss_feeds = [{'title':_("New Media"),
                        'link':h.url_for(controller='medium', action='new_media_rss')},
                       {'title':_("Updated Media"),
                        'link':h.url_for(controller='medium', action='updated_media_rss')}]
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
        return self.delete_many()

    def delete_many(self):
        for item in h.checkboxes(request, 'item_id_'):
            db_item = meta.find(model.Medium, item)
            meta.Session.delete(db_item)
            h.flash(_("deleted: %s") % db_item.title)

        meta.Session.commit()

        return redirect(url(controller='medium', action='index'))

    def delete_one(self, id):
        log.debug("delete_one(%s)" % id)
        db_item = meta.find(model.Medium, id)
        meta.Session.delete(db_item)
        meta.Session.commit()
        h.flash(_("deleted: %s") % db_item.title)
        ret_to = request.params.get('return_to')
        log.debug("ret_to: %s" % ret_to)
        if ret_to and ret_to != None:
            return redirect(str(request.params.get('return_to')))
        else:
            return redirect(url(controller='medium', action='index'))

    def edit(self, id, mobile=False):
        log.debug("id: %s" % id)
        log.debug("mobile: %s" % mobile)
        #~ log.debug("DEBUG: %s" % url(controller='medium', action='edit', id=id, mobile=True))
        #~ log.debug("DEBUG: %s" % url(controller='medium', action='edit', id=id, mobile=False))
        #~ log.debug("DEBUG: %s" % url(controller='medium', action='edit', id=id))
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

        for relation_name in c.persons:
            log.debug("relation_name: %s" % relation_name)
            #~ log.debug("relation_name: %s" % c.persons[relation_name])

            c.persons[relation_name].sort(key=lambda x: len(x.person.persons_to_media))
            c.persons[relation_name].reverse()

            for item in c.persons[relation_name]:
                log.debug("item: %d - %s" % (len(item.person.persons_to_media),
                                             item.person))

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

        if mobile:
            return render('mobile/medium/edit.mako')
        else:
            return render('medium/edit.mako')

    def edit_post(self):
        id = request.params.get('id')
        item = meta.find(model.Medium, id)
        item.title = request.params.get('title')
        item.image_url = request.params.get('image_url')
        item.updated_ts = datetime.now()
        item.set_tagstring(request.params.get('tags'))
        meta.Session.add(item)
        meta.Session.commit()
        h.flash(_("updated: '%s'") % item.title)

        return_to = request.params.get('return_to')
        log.debug("return_to: %s" % return_to)
        if return_to:
            return redirect(str(return_to))
        else:
            return redirect(url(controller='medium', action='edit', id=id))

    def next_without_image(self, id):
        query = meta.Session\
            .query(model.Medium)\
            .filter(model.Medium.image_data == None)\
            .filter(model.Medium.id < id)\
            .order_by(model.Medium.id.desc())

        medium = query.first()
        if not medium:
            h.flash(_("all media after this have an image"))
            return redirect(url(controller='medium', action='edit', id=id))

        return_to=request.params.get('return_to')
        if return_to:
            return redirect(url(controller='medium', action='edit', id=medium.id, return_to=request.params.get('return_to')))
        else:
            return redirect(url(controller='medium', action='edit', id=medium.id))

    def debug(self):
        log.debug("START DEBUG")
        #~ h.flash(u"testing \xc3\xa4")
        h.flash("<i>blah</i>", False)
        return redirect(url(controller='medium', action='index'))
        
    def set_view_options(self, type=None, tag=None):
        items_per_page = request.params.get('items_per_page')
        if not items_per_page or int(items_per_page) <= 0:
            h.flash(_("'Number of images' must be greater then null"))
            return redirect(url(controller='medium', action='list_gallery', type=type, tag=tag))

        items_per_page = int(items_per_page)
        h.flash(_("%d images will be display for now on") % items_per_page)
        session['items_per_page'] = items_per_page
        session.save()

        #~ h.flash("session, items_per_page: %s" % session['items_per_page'])
        return redirect(url(controller='medium', action='list_gallery', type=type, tag=tag))
        
    def new_media_rss(self):
        query = meta.Session.query(model.Medium)\
                            .order_by(model.Medium.created_ts.desc())
        return self.__create_feed__(query, _("New Media"), 'created_ts')

    def updated_media_rss(self):
        query = meta.Session.query(model.Medium)\
                            .order_by(model.Medium.updated_ts.desc())
        return self.__create_feed__(query, _("Updated Media"), 'updated_ts')

    def __create_feed__(self, query, title, key_field):
        myItems = []
        base_url = config.get('base_url', 'http://127.0.0.1:5000')
        query = query.limit(10)


        template = h.tmpl('/medium/rss_item.mako', 'description')

        for item in query.all():
            newItem = PyRSS2Gen.RSSItem(
                title = item.title,
                link = base_url + h.url_for(controller='/medium', action="edit", id=item.id),
                description = template.render_unicode(item, h, base_url),
                #~ guid = PyRSS2Gen.Guid(str(item.id)),
                guid = PyRSS2Gen.Guid("%s, %s" % (item.id, item.__dict__[key_field])),
                pubDate = item.__dict__[key_field])

            myItems.append(newItem)


        rss = PyRSS2Gen.RSS2(
            title = title,
            link = base_url + h.url_for(controller='/medium', action='list'),
            description = _("New Media"),
            lastBuildDate = datetime.now(),
            items = myItems)

        return rss.to_xml(encoding="utf-8")

