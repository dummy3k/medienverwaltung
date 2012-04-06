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
            if k.startswith('repoze.'):
                log.debug("environ[%s] = %s" % (k, v))
        identity = environ.get('repoze.who.identity')
        log.debug("identity: %s" % identity)
        if identity:
            #~ if type
            user_id = identity['repoze.who.userid']
            log.debug("user_id: %s" % user_id)
            log.debug("type(user_id): %s" % type(user_id))
            if type(user_id) == model.User:
                log.debug("setting c.user to identity['repoze.who.userid']")
                c.user = user_id
            else:
                openid_model = meta.Session\
                                .query(model.UserOpenId)\
                                .filter(model.UserOpenId.openid==user_id)\
                                .first()
                if openid_model:
                    log.debug("user is logged via opendid: %s" % user_id)
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
