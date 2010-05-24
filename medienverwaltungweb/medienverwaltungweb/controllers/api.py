import logging
import amazonproduct
from datetime import datetime
import urllib
from StringIO import StringIO

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.controllers import XMLRPCController
from pylons import config

import medienverwaltungweb.model as model
import medienverwaltungweb.lib.helpers as h
import medienverwaltungweb.lib.amazon as amazon
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta
from medienverwaltungcommon.amazon import add_persons

log = logging.getLogger(__name__)

class ApiController(XMLRPCController):
    def index(self):
        return "API Interface"
        
    def sayhello(self, s):
        return 'Hello %s' % s
    sayhello.signature = [ ['struct', 'string'] ]

    def AddMediumByISBN(self, isbn, search_index):
        return amazon.AddMediumByISBN(isbn, search_index)
    AddMediumByISBN.signature = [ ['struct', 'string', 'string'] ]
