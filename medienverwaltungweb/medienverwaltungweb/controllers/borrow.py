import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons import url
from pylons.controllers.util import abort, redirect
from pylons.i18n import _
from webhelpers import paginate

from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta
import medienverwaltungweb.model as model
import medienverwaltungweb.lib.helpers as h

log = logging.getLogger(__name__)

class BorrowController(BaseController):
    def index(self):
        return self.list_borrowed_media()

    def checkout(self, id):
        c.item = meta.find(model.Medium, id)
        c.borrowers = meta.Session\
                          .query(model.Borrower)\
                          .order_by(model.Borrower.id.desc())\
                          .all()
        return render('borrow/borrow.mako')

    def checkout_post(self):
        borrower_id = int(request.params.get('borrower'))

        if not borrower_id or int(borrower_id) < 0:
            log.debug("redirect because no borrower_id")

            ids = ','.join(h.checkboxes(request, 'item_id_'))
            log.debug("ids: %s" % ids)
            return redirect(url(controller='borrow', action='add_borrower', media_ids=ids))
        else:
            borrower = meta.Session.query(model.Borrower).get(borrower_id)
            if not borrower:
                raise Exception("could not find borrower '%d'" % borrower_id)

        log.debug("borrower_id: %s" % borrower_id)
        for item in h.checkboxes(request, 'item_id_'):
            log.debug("checkout: %s" % item)
            self.__checkout_post__(item, borrower)

        meta.Session.commit()
        return redirect(url(controller='borrow', action='edit_borrower', id=borrower_id))

    def __checkout_post__(self, media_id, borrower):
        log.debug("")
        log.debug("media_id: %s" % media_id)
        log.debug("borrower_id: %s" % borrower.id)

        log.debug("FOLLOW ME, too, too")
        record = model.BorrowAct()
        record.media_id = media_id
        #~ record.borrower_id = borrower_id
        record.borrowed_ts = datetime.now()
        #~ meta.Session.add(record)

        borrower.acts.append(record)

        medium = meta.Session.query(model.Medium).get(media_id)
        if not medium:
            raise Exception("could not find medium: %s" % media_id)

        borrower_link = h.tmpl('borrow/snippets.mako', 'link_to_borrower')\
                         .render_unicode(item=borrower, h=h)
        medium_link = h.tmpl('medium/snippets.mako', 'link_to_medium')\
                       .render_unicode(item=medium, h=h)
        h.flash(_("%(medium)s borrowed to %(to)s") % {'medium':medium_link,
                                                      'to':borrower_link},
                escape=False)

    def add_borrower(self):
        c.item = model.Borrower()
        c.post_action = "add_borrower_post"
        c.media_id = request.params.get('media_id')
        return render('borrow/add_borrower.mako')

    def add_borrower_post(self):
        log.debug("add_borrower_post")

        record = model.Borrower()
        record.first_name = request.params.get('first_name')
        record.last_name = request.params.get('last_name')
        record.email = request.params.get('email')
        record.created_ts = datetime.now()
        record.updated_ts = datetime.now()
        meta.Session.add(record)
        #~ meta.Session.commit()
        log.debug("record.id: %s" % record.id)

        h.flash(_("added: '%s %s'") % (record.first_name, record.last_name))
        media_ids = request.params.get('media_ids')
        log.debug("media_ids %s "% media_ids)
        if not media_ids:
            meta.Session.commit()
            return redirect(url(controller='borrow', action='list_borrowers'))
        else:
            log.debug("FOLLOW ME, media_id: %s" % media_ids)
            log.debug("url: %s" % h.url_for(controller='borrow', action='edit_borrower', id=record.id))
            for item in request.params.get('media_ids').split(','):
                log.debug("checkout: %s" % item)
                self.__checkout_post__(item, record)

            meta.Session.commit()
            return redirect(url(controller='borrow', action='edit_borrower', id=record.id))

    def list_borrowers(self, page=1):
        query = meta.Session\
            .query(model.Borrower)\
            .order_by(model.Borrower.id.desc())

        #~ c.items = query.all()
        c.page = paginate.Page(query, page)
        c.title = _("All borrowers")
        c.pager_action = 'list_borrowers'
        return render('borrow/list_borrowers.mako')

    def edit_borrower(self, id):
        c.item = meta.find(model.Borrower, id)
        c.borrowed_media = meta.Session\
                          .query(model.BorrowAct)\
                          .filter(model.BorrowAct.borrower_id == id)\
                          .filter(model.BorrowAct.returned_ts == None)\
                          .order_by(model.BorrowAct.id.desc())\
                          .all()

        c.pager_action = 'edit_borrower'
        if c.mobile:
            return render('mobile/borrow/edit_borrower.mako')
        else:
            return render('borrow/edit_borrower.mako')

    def edit_borrower_post(self, id):
        record = meta.find(model.Borrower, id)
        record.first_name = request.params.get('first_name')
        record.last_name = request.params.get('last_name')
        record.email = request.params.get('email')
        record.updated_ts = datetime.now()
        meta.Session.add(record)
        meta.Session.commit()

        h.flash(_("updated: %s") % record)
        return redirect(url(controller='borrow', action='edit_borrower', id=id))

    def delete_borrower_post(self, id):
        record = meta.find(model.Borrower, id)
        meta.Session.delete(record)
        meta.Session.commit()

        h.flash(_("deleted: '%s %s'") % (record.first_name, record.last_name))
        return redirect(url(controller='borrow', action='list_borrowers'))

    def show_history(self, id, page=1):
        c.item = meta.find(model.Borrower, id)
        query = meta.Session\
                          .query(model.BorrowAct)\
                          .filter(model.BorrowAct.borrower_id == id)\
                          .order_by(model.BorrowAct.id.desc())

        c.page = paginate.Page(query, page)
        c.title = _("Borrow History")
        return render('borrow/history.mako')

    def checkin_post(self):
        #~ id = request.params.get('id')
        #~ borrower = meta.find(model.Borrower, id)
        for item in h.checkboxes(request, 'item_id_'):
            record = meta.Session.query(model.BorrowAct).get(item)
            if not record:
                raise Exception("could not find BorrowAct '%s'" % item)

            record.returned_ts = datetime.now()
            meta.Session.add(record)
            borrower_link = h.tmpl('borrow/snippets.mako', 'link_to_borrower')\
                             .render_unicode(item=record.borrower, h=h)
            medium_link = h.tmpl('medium/snippets.mako', 'link_to_medium')\
                           .render_unicode(item=record.medium, h=h)
            h.flash(_("%s has returned medium '%s'") % (borrower_link, medium_link),
                    escape=False)

        meta.Session.commit()
        return redirect(url(controller='borrow', action='index'))

    def list_borrowed_media(self):
        c.borrow_acts = meta.Session.query(model.BorrowAct)\
                                    .filter(model.BorrowAct.returned_ts == None)\
                                    .all()
        return render('borrow/list_borrowed_media.mako')

    def scanner(self):
        return render('borrow/scanner.mako')

    def scanner_post(self):
        c.available = []
        c.borrowed = []
        for line in request.params.get('isbns').split('\n'):
            line = line.strip()
            if line:
                medium = meta.Session\
                             .query(model.Medium)\
                             .filter(model.Medium.isbn == line)\
                             .first()

                if not medium:
                    h.flash(_("Isbn '%s' not found") % line)
                else:
                    borrow_act = meta.Session\
                                     .query(model.BorrowAct)\
                                     .filter(model.BorrowAct.media_id == medium.id)\
                                     .filter(model.BorrowAct.returned_ts == None)\
                                     .first()
                    if borrow_act:
                        c.borrowed.append(borrow_act)
                    else:
                        c.available.append(medium)

        c.borrowers = meta.Session.query(model.Borrower).all()
        return render('borrow/scanner_post.mako')

