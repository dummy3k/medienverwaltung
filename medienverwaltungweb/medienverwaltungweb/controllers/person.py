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
    def index(self, id=None):
        if id:
            return self.edit(id)
        else:
            return 'Hello World. Need id.'

    def edit(self, id, page=1):
        c.item = meta.find(model.Person, id)

        query = meta.Session\
            .query(model.PersonToMedia)\
            .filter(model.PersonToMedia.person_id == id)
        c.page = paginate.Page(query, page)
        return render('person/display.mako')

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
        meta.Session.add(relation)
        meta.Session.commit()

        h.flash("added: %(person)s to %(medium)s" % {'person':person.name,
                                                     'medium':medium.title})
        return redirect_to(controller='medium', action='edit', id=id)
        
