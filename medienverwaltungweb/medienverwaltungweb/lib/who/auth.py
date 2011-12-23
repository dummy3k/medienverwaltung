import logging

log = logging.getLogger(__name__)

class UserModelPlugin(object):

    def authenticate(self, environ, identity):
        log.debug("authenticate(identity: %s)" % identity)
        try:
            username = identity['login']
            password = identity['password']
        except KeyError:
            return None

        #~ success = model.User.authenticate(username, password)
        if username == 'a' and password == 'a':
            return username
        else:
            return None

        #~ success = username == 'a' and password == 'aa'
        #~ log.debug("success: %s" % success)
        #~ return success

    #~ def add_metadata(self, environ, identity):
        #~ username = identity.get('repoze.who.userid')
        #~ user = model.User.get(username)
        #~
        #~ if user is not None:
            #~ identity['user'] = user
