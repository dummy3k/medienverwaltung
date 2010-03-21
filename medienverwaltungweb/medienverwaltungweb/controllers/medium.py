import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import medienverwaltungweb.model as model
import medienverwaltungweb.lib.helpers as h
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta


log = logging.getLogger(__name__)

class MediumController(BaseController):

    def index(self):
        return self.mass_add()

    def mass_add(self):
        return render('medium/mass_add.mako')

    def mass_add_post(self):
        if not request.params.get('title'):
            h.flash("please specify name")
            return redirect_to(action='mass_add')

        record = model.Medium()
        record.title = request.params.get('title')
        meta.Session.save(record)
        meta.Session.commit()

        h.flash("added: %s" % record)
        return redirect_to(action='index')
