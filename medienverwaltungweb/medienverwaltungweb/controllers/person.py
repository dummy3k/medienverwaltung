import logging

from webhelpers import paginate
import urllib
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.i18n import _, ungettext
from sqlalchemy import func
from sqlalchemy.sql import select, join, and_, or_, not_

from medienverwaltungweb.lib.base import BaseController, render
import medienverwaltungweb.model as model
from medienverwaltungweb.model import meta
import medienverwaltungweb.lib.helpers as h

log = logging.getLogger(__name__)

class PersonController(BaseController):
    def edit(self, id, page=1):
        c.item = meta.find(model.Person, id)

        query = meta.Session\
                    .query(model.PersonToMedia)\
                    .join(model.Medium)\
                    .filter(model.PersonToMedia.person_id == id)\
                    .order_by(model.Medium.title)
            
        c.page = paginate.Page(query, page)
        return render('person/display.mako')

    def edit_post(self, id):
        item = meta.Session.query(model.Person).get(id)
        if request.params.get("create_alias"):
            alias = model.PersonAlias()
            alias.name = item.name
            item.aliases.append(alias)
            
        item.name = request.params.get("name")
        
        meta.Session.commit()
        h.flash(_("updated: '%s'") % item.name)
        return redirect_to(controller='person', action='edit', id=id)
        
    def list(self, page=1):
        relation_type = request.params.get('role')
        query = meta.Session.query(model.Person)
        if relation_type:
            query = query.join(model.PersonToMedia)\
                         .join(model.RelationType)\
                         .filter(model.RelationType.name == relation_type)
                         
        c.page = paginate.Page(query, page)

        if relation_type == 'Actor':
            c.title = _("Actor")
        elif relation_type == 'Director':
            c.title = _("Directors")
        elif relation_type == 'Author':
            c.title = _("Authors")
        elif relation_type:
            c.title = _("Persons of type '%s'") % relation_type
        else:
            c.title = _("Every Person")
            
        if page > 1:
            c.title += _(", page %s") % c.page.page

        c.pager_action = "list"
        return render('person/list.mako')

    def top_ten(self):
        #
        id_col = model.person_to_media_table.c.person_id
        cnt_col = func.count()

        query = select([id_col, cnt_col], from_obj=[model.relation_types_table])\
                .where(model.relation_types_table.c.name == 'Actor')\
                .where(model.person_to_media_table.c.type_id == model.relation_types_table.c.id)\
                .group_by(id_col)\
                .order_by(cnt_col.desc())\
                .limit(10)

        query.bind = meta.engine
        c.actors = map(lambda x: (meta.find(model.Person, x[0]), x[1]), query.execute())


        query = select([id_col, cnt_col], from_obj=[model.relation_types_table])\
                .where(model.relation_types_table.c.name == 'Director')\
                .where(model.person_to_media_table.c.type_id == model.relation_types_table.c.id)\
                .group_by(id_col)\
                .order_by(cnt_col.desc())\
                .limit(10)

        query.bind = meta.engine
        c.directors = map(lambda x: (meta.find(model.Person, x[0]), x[1]), query.execute())

        query = select([id_col, cnt_col], from_obj=[model.relation_types_table])\
                .where(model.relation_types_table.c.name == 'Author')\
                .where(model.person_to_media_table.c.type_id == model.relation_types_table.c.id)\
                .group_by(id_col)\
                .order_by(cnt_col.desc())\
                .limit(10)

        query.bind = meta.engine
        c.authors = map(lambda x: (meta.find(model.Person, x[0]), x[1]), query.execute())

        return render('person/top_ten.mako')

    def add_to_medium_post(self, id):
        medium = meta.Session.query(model.Medium).get(id)
        name = request.params.get('name')
        if len(name.strip()) == 0:
            h.flash(_("Please enter the persons name"))
            return redirect_to(controller='medium', action='edit', id=id)

        person = meta.Session.query(model.Person)\
                             .filter(model.Person.name == name)\
                             .first()

        relation = meta.Session.query(model.RelationType)\
                       .filter(model.RelationType.name == request.params.get('role'))\
                       .first()
        if not relation:
            return "unknown relation: %s" % relation
            
        if not person:
            person = model.Person()
            person.name = name
            meta.Session.add(person)

        media2person = model.PersonToMedia()
        medium.persons_to_media.append(media2person)
        person.persons_to_media.append(media2person)
        relation.persons_to_media.append(media2person)
        meta.Session.add(media2person)
        meta.Session.commit()

        h.flash(_("added: %(person)s to %(medium)s") % {'person':person.name,
                                                        'medium':medium.title})
        return redirect_to(controller='medium', action='edit', id=id)
        
    def remove_from_media(self, id):
        item = meta.Session.query(model.PersonToMedia).get(id)
        meta.Session.delete(item)

        h.flash(_("removed: %(person)s from %(medium)s") % {'person':item.person.name,
                                                            'medium':item.medium.title})
        meta.Session.commit()
        return redirect_to(controller='medium', action='edit', id=item.medium.id)
    def merge(self):
        person_ids = h.checkboxes(request, 'person_id_')

        c.persons = meta.Session\
                       .query(model.Person)\
                       .filter(model.Person.id.in_(person_ids))\
                       .all()
        c.person_ids_str = ",".join(person_ids)
        return render('person/merge.mako')
        
    def merge_post(self):
        primary_id = int(request.params.get('primary_id'))
        primary = meta.Session.query(model.Person).get(primary_id)
        log.debug("primary: %s" % primary)

        primary_media = map(lambda x: x.medium, primary.persons_to_media)
        log.debug("primary_media: %s" % primary_media)

        person_ids = request.params.get('person_ids_str')
        person_ids = person_ids.split(',')
        person_ids = map(lambda x: int(x), person_ids)
        person_ids.remove(primary_id)
        log.debug("person_ids: %s" % person_ids)

        remap_cnt = 0
        for secondary_id in person_ids:
            secondary = meta.Session.query(model.Person).get(secondary_id)
            log.debug("secondary: %s" % secondary)
            for item in secondary.persons_to_media:
                if item.medium in primary_media:
                    log.debug("medium already exists: %s" % item.medium)
                else:
                    log.debug("medium does not exists: %s" % item.medium)
                    #~ item.person_id = primary.id
                    #~ meta.Session.update(item)
                    record = model.PersonToMedia()
                    record.type_id = item.type_id
                    item.medium.persons_to_media.append(record)
                    primary.persons_to_media.append(record)
                    
                    remap_cnt += 1

            alias = model.PersonAlias()
            alias.name = secondary.name
            primary.aliases.append(alias)
            meta.Session.delete(secondary)

        meta.Session.commit()
        #~ h.flash(_("Removed %(person_cnt)d, added %(media_cnt)d media") %\
                #~ {'person_cnt':len(person_ids), 'media_cnt':remap_cnt})

        h.flash(ungettext("Removed %d person",
                          "Removed %d persons",
                          len(person_ids)) % len(person_ids))
                          
        h.flash(ungettext("Added %(cnt)d medium to '%(person)s'",
                          "Added %(cnt)d media to '%(person)s'",
                          remap_cnt) % {'cnt':remap_cnt,
                                             'person':primary.name})
                          
        return_to = request.params.get('return_to',
                                       h.url_for(controller='person',
                                                 action='edit',
                                                 id=primary.id))
        return redirect_to(str(return_to))
        
