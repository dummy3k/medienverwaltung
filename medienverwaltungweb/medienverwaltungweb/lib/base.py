"""The base Controller API

Provides the BaseController class for subclassing.
"""
import logging

from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons.i18n import get_lang, set_lang
from pylons import config, request
from pylons import tmpl_context as c
from pylons.controllers.util import abort, redirect

import medienverwaltungweb.model as model
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

        for k, v in environ.items():
            log.debug("environ[%s] = %s" % (k, v))
        identity = environ.get('repoze.who.identity')
        if identity:
            openid = identity['repoze.who.userid']
            log.debug("openid: %s" % openid)
            openid_model = meta.Session\
                            .query(model.UserOpenId)\
                            .filter(model.UserOpenId.openid==openid)\
                            .first()
            if openid_model:
                log.debug("!!!!!!!!!")
                c.user = openid_model.user

        log.debug("__call__(): %s" % environ['pylons.routes_dict'])
        if 'mobile' in environ['pylons.routes_dict']:
            c.mobile = (environ['pylons.routes_dict']['mobile'] == u'True')
        else:
            c.mobile = False

        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()

    def login_user(self):
        identity = request.environ.get('repoze.who.identity')
        if not identity:
            # Force skip the StatusCodeRedirect middleware; it was stripping
            #   the WWW-Authenticate header from the 401 response
            request.environ['pylons.status_code_redirect'] = True
            abort(401, 'You are not authenticated')

    def __before__(self):
        log.debug("__before__()")


    @property
    def allow_openid(self):
        return True
