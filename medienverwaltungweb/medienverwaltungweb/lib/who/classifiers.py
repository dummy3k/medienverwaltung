import logging
import zope.interface
from repoze.who.interfaces import IChallengeDecider
from repoze.who.interfaces import IRequestClassifier

import repoze.who.classifiers

log = logging.getLogger(__name__)


#def openid_challenge_decider(environ, status, headers):
    ##~ log.debug("environ: %s" % environ)
    ##~ log.debug("status: %s" % status)
    ##~ log.debug("headers: %s" % headers)
    ##~ log.debug("'pylons.action_method': %s" % environ['pylons.action_method'])
    ##~ log.debug("'pylons.controller': %s" % environ['pylons.controller'])
    ##~ log.debug("'pylons.controller': %s" % environ['pylons.controller'].allow_openid)


    ## we do the default if it's a 401, probably we show a form then
    #if status.startswith('401 '):
        #if not environ['pylons.controller'].allow_openid:
            #return False
        #return True
    #elif environ.has_key('repoze.whoplugins.openid.openid'):
        ## in case IIdentification found an openid it should be in the environ
        ## and we do the challenge
        #return True
    #return False

#zope.interface.directlyProvides(openid_challenge_decider, IChallengeDecider)

def default_request_classifier(environ):
    """ Returns one of the classifiers 'api',
    depending on the imperative logic below"""
    log.debug("default_request_classifier(%s)" % environ)

    if environ['PATH_INFO'].startswith('/JsonApi/'):
        return 'api'

    return repoze.who.classifiers.default_request_classifier(environ)

zope.interface.directlyProvides(default_request_classifier, IRequestClassifier)

