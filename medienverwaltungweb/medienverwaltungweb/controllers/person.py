import logging

from webhelpers import paginate
import urllib
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from medienverwaltungweb.lib.base import BaseController, render
import medienverwaltungweb.model as model
from medienverwaltungweb.model import meta

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
            .query(model.Medium)\
            .join(model.PersonToMedia)\
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

        if relation_type:
            c.title = "All %ss" % relation_type
        else:
            c.title = "Every Person"
            
        c.pager_action = "list"
        return render('person/list.mako')

