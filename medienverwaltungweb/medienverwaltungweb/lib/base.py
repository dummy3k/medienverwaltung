"""The base Controller API

Provides the BaseController class for subclassing.
"""
import logging

from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons.i18n import get_lang, set_lang
from pylons import config
from pylons import tmpl_context as c

from medienverwaltungweb.model import meta

log = logging.getLogger(__name__)

class BaseController(WSGIController):

    def __init__(self):
        lng = config['language']
        if lng != "en":
            set_lang(lng)
        
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        log.debug("__call__(): %s" % environ['pylons.routes_dict'])
        if 'mobile' in environ['pylons.routes_dict']:
            c.mobile = (environ['pylons.routes_dict']['mobile'] == u'True')
        else:
            c.mobile = False
            
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()

        
    def __before__(self):
        log.debug("__before__()")
        
