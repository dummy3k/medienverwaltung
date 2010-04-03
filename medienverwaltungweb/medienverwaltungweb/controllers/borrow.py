import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.i18n import _
from webhelpers import paginate

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

    def checkout(self, id):
        c.item = meta.find(model.Medium, id)
        c.borrowers = meta.Session\
                          .query(model.Borrower)\
                          .order_by(model.Borrower.id.desc())\
                          .all()
        return render('borrow/borrow.mako')

    def checkout_post(self):
        media_id = request.params.get('media_id')
        borrower_id = request.params.get('borrower')
        self.__checkout_post__(media_id, borrower_id)
        return redirect_to(controller='borrow', action='edit_borrower', id=borrower_id)
        
    def __checkout_post__(self, media_id, borrower_id):
        log.debug("__checkout_post__")
        log.debug("media_id: %s" % media_id)
        log.debug("borrower_id: %s" % borrower_id)
        if not borrower_id or int(borrower_id) < 0:
            log.debug("redirect because no borrower_id")
            return redirect_to(controller='borrow', action='add_borrower', media_id=media_id)
            
        log.debug("FOLLOW ME, too, too")
        record = model.BorrowAct()
        record.media_id = media_id
        record.borrower_id = borrower_id
        record.borrowed_ts = datetime.now()
        meta.Session.save(record)
        meta.Session.commit()

        borrower_link = h.tmpl('borrow/snippets.mako', 'link_to_borrower')\
                         .render(item=record.borrower, h=h)
        medium_link = h.tmpl('medium/snippets.mako', 'link_to_medium')\
                       .render(item=record.medium, h=h)
        h.flash(_("%s borrowed to %s") % (medium_link,
                                            borrower_link))
        
    def add_borrower(self):
        c.item = model.Borrower()
        c.post_action = "add_borrower_post"
        c.media_id = request.params.get('media_id')
        return render('borrow/add_borrower.mako')
        
    def add_borrower_post(self):
        record = model.Borrower()
        record.first_name = request.params.get('first_name')
        record.last_name = request.params.get('last_name')
        record.email = request.params.get('email')
        record.created_ts = datetime.now()
        record.updated_ts = datetime.now()
        meta.Session.add(record)
        meta.Session.commit()
        log.debug("record.id: %s" % record.id)

        h.flash(_("added: %s") % record)
        media_id = request.params.get('media_id')
        log.debug("media_id %s "% media_id)
        if not media_id:
            return redirect_to(controller='borrow', action='list_borrowers')
        else:
            log.debug("FOLLOW ME, media_id: %s" % media_id)
            log.debug("url: %s" % h.url_for(controller='borrow', action='edit_borrower', id=record.id))
            self.__checkout_post__(media_id, record.id)
            return redirect_to(controller='borrow', action='edit_borrower', id=record.id)
            #~ return redirect_to(controller='borrow',
                               #~ action='checkout_post',
                               #~ borrower_id=record.id,
                               #~ media_id=media_id)
            #~ return self.checkout_post()

    def list_borrowers(self, page=1):
        query = meta.Session\
            .query(model.Borrower)\
            .order_by(model.Borrower.id.desc())

        #~ c.items = query.all()
        c.page = paginate.Page(query, page)
        c.title = _("All borrowers")
        #~ c.pager_action = "list_no_image"
        return render('borrow/list_borrowers.mako')
    
    def edit_borrower(self, id):
        c.item = meta.find(model.Borrower, id)
        c.borrowed_media = meta.Session\
                          .query(model.Medium)\
                          .join(model.BorrowAct)\
                          .filter(model.BorrowAct.borrower_id == id)\
                          .filter(model.BorrowAct.returned_ts == None)\
                          .order_by(model.BorrowAct.id.desc())\
                          .all()
        
        return render('borrow/edit_borrower.mako')
        
    def edit_borrower_post(self, id):
        record = meta.find(model.Borrower, id)
        record.first_name = request.params.get('first_name')
        record.last_name = request.params.get('last_name')
        record.email = request.params.get('email')
        record.updated_ts = datetime.now()
        meta.Session.update(record)
        meta.Session.commit()

        h.flash(_("updated: %s") % record)
        return redirect_to(controller='borrow', action='edit_borrower', id=id)

    def delete_borrower_post(self, id):
        record = meta.find(model.Borrower, id)
        meta.Session.delete(record)
        meta.Session.commit()

        h.flash(_("deleted: %s") % record)
        return redirect_to(controller='borrow', action='list_borrowers')

    def show_history(self, id, page=1):
        c.item = meta.find(model.Borrower, id)
        query = meta.Session\
                          .query(model.BorrowAct)\
                          .filter(model.BorrowAct.borrower_id == id)\
                          .order_by(model.BorrowAct.id.desc())
        
        c.page = paginate.Page(query, page)
        c.title = _("Borrow History")
        return render('borrow/history.mako')

    def checkin_post(self, id):
        #~ borrower = meta.find(model.Borrower, id)
        for item in h.checkboxes(request, 'item_id_'):
            record = meta.Session\
                         .query(model.BorrowAct)\
                         .filter(model.BorrowAct.borrower_id == id)\
                         .filter(model.BorrowAct.media_id == item)\
                         .first()
                         
            record.returned_ts = datetime.now()
            meta.Session.update(record)
            borrower_link = h.tmpl('borrow/snippets.mako', 'link_to_borrower')\
                             .render(item=record.borrower, h=h)
            medium_link = h.tmpl('medium/snippets.mako', 'link_to_medium')\
                           .render(item=record.medium, h=h)
            h.flash(_("%s has returned medium '%s'") % (borrower_link, medium_link))

        #~ meta.Session.commit()

        return redirect_to(action='show_history')
        
