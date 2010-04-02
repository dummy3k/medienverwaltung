import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta
import medienverwaltungweb.model as model
import medienverwaltungweb.lib.helpers as h

log = logging.getLogger(__name__)

class BorrowController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/borrow.mako')
        # or, return a response
        return 'Hello World'

    def borrow(self, id):
        c.item = meta.find(model.Medium, id)
        return render('borrow/borrow.mako')

    def borrow_post(self):
        id = request.params.get('id')
        borrower_id = request.params.get('borrower')
        return str(borrower_id)
        
    def add_borrower(self):
        return render('borrow/add_borrower.mako')
        
    def add_borrower_post(self):
        record = model.Borrower()
        record.first_name = request.params.get('first_name')
        record.last_name = request.params.get('last_name')
        record.email = request.params.get('email')
        record.created_ts = datetime.now()
        record.updated_ts = datetime.now()
        meta.Session.save(record)
        meta.Session.commit()

        h.flash("added: %s" % record)
        return redirect_to(controller='borrow', action='add_borrower')

    def list_borrowers(self, page=1):
        query = meta.Session\
            .query(model.Borrower)
            .order_by(model.Borrower.id.desc())

        #~ c.items = query.all()
        c.page = paginate.Page(query, page)
        #~ c.title = "Media without images"
        #~ c.pager_action = "list_no_image"
        return render('medium/list_borrowers.mako')
    
