import logging

from pylons import request, response, session, tmpl_context as c
from pylons import url
from pylons.controllers.util import abort, redirect

from medienverwaltungweb.lib.base import BaseController, render

log = logging.getLogger(__name__)

class TagController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/tag.mako')
        # or, return a response
        return 'Hello World'


    #~ def 
