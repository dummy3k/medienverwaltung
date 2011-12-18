import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

import medienverwaltungweb.model as model
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta

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

        openid_model = meta.Session\
                        .query(model.UserOpenId)\
                        .filter(model.UserOpenId.openid==openid)\
                        .first()

        if not openid_model:
            user_model = model.User()
            user_model.name = openid

            openid_model = model.UserOpenId()
            meta.Session.add(user_model)
            meta.Session.commit()
            log.info("new: %s" % user_model)

            openid_model.user_id = user_model.id
            openid_model.openid = openid

            meta.Session.add(openid_model)
            meta.Session.commit()
            log.info("new: %s" % openid_model)

        openid_model.user.last_login = datetime.now()
        meta.Session.add(openid_model.user)
        meta.Session.commit()

        redirect("/")
        #~ return "success: %s" % openid

    def logout_success(self):
        redirect("/")
        #~ return "logout_success"

