import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

import medienverwaltungweb.model as model
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta

log = logging.getLogger(__name__)

class MobileController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/mobile.mako')
        # or, return a string
        return 'Hello World'

    def lookup(self):
            #~ query = meta.Session\
                #~ .query(model.Medium)\
                #~ .filter(or_(model.Medium.title==item,
                            #~ model.Medium.isbn==item))

        isbn = request.params.get('q')
        c.item = meta.Session.query(model.Medium)\
                             .filter(model.Medium.isbn==isbn)\
                             .first()
                             
        return render('mobile/lookup.mako')
        return request.params.get('q')
