import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from medienverwaltungweb.lib.base import BaseController, render
import medienverwaltungweb.lib.helpers as h
from medienverwaltungweb.model import meta
import medienverwaltungweb.model as model

log = logging.getLogger(__name__)

class SearchController(BaseController):

    def index(self):
        return render('search/index.mako')

    def search_post(self):
        query = request.params.get('query')
        if not query:
            h.flash("please enter search query")
            return redirect_to(action='index')

        like_query = "%%%s%%" % query
        media_query = meta.Session\
                          .query(model.Medium)\
                          .filter(model.Medium.title.like(like_query))
        c.media_result = media_query.all()

        persons_query = meta.Session\
                          .query(model.Person)\
                          .filter(model.Person.name.like(like_query))
        c.persons_result = persons_query.all()

        return render('search/results.mako')
        
