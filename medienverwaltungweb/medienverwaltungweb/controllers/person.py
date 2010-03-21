import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from medienverwaltungweb.lib.base import BaseController, render
import medienverwaltungweb.model as model
from medienverwaltungweb.model import meta

log = logging.getLogger(__name__)

class PersonController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/actor.mako')
        # or, return a response
        return 'Hello World'

    def display(self, id):
        c.item = meta.find(model.Person, id)
        return render('person/display.mako')

    def list(self):
        query = meta.Session.query(model.Person)
        c.items = query.all()
        return render('person/list.mako')

