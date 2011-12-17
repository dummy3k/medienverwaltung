import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from medienverwaltungweb.lib.base import BaseController, render

log = logging.getLogger(__name__)

class LoginController(BaseController):

    def index(self):
        identity = request.environ.get('repoze.who.identity')
        log.debug("identity: %s" % identity)
        for item in request.environ:
            if item.startswith('repoze'):
                log.debug(item)
            if 'openid_field' in item:
                log.debug(item)


        if not identity:
            #~ request.environ['openid'] = 'http://myopenid.com/schraube4711'
            abort(401, 'You are not authenticated')

        for item in identity:
            print "identity.%s: %s" % (item, identity[item])

        openid = identity['repoze.who.userid']
        return 'Hello %s' % openid


    def login_form(self, came_from=None):
        c.openid = 'http://dummy4711.myopenid.com/'
        c.came_from_field = request.params.get('came_from')
        return render('login/login_form.mako')

    def do_login(self):
        return "do_login"

    def success(self):
        identity = request.environ.get('repoze.who.identity')
        if not identity:
            abort(401, 'You are not authenticated')
        openid = identity['repoze.who.userid']
        return "success: %s" % openid

    def logout_success(self):
        return "logout_success"

