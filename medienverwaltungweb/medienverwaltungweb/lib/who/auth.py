import logging
import hashlib
import medienverwaltungweb.model as model
from medienverwaltungweb.model import meta

log = logging.getLogger(__name__)

class UserModelPlugin(object):

    def authenticate(self, environ, identity):
        log.debug("authenticate(identity: %s)" % identity)
        try:
            username = identity['login']
            password = identity['password']
        except KeyError:
            return None

        user_model = meta.Session\
                        .query(model.User)\
                        .filter(model.User.name==username)\
                        .first()

        if not user_model:
            log.debug("unkown user: %s" % username)
            return None
        else:
            hasher = hashlib.sha1()
            hasher.update(str(user_model.pwd_salt))
            hasher.update(password)
            pwd_hash = hasher.hexdigest()

            if user_model.pwd_hash == pwd_hash:
                return user_model
            else:
                log.debug("bad password '%s' for user '%s'" %\
                    (password, username))


    #~ def add_metadata(self, environ, identity):
        #~ username = identity.get('repoze.who.userid')
        #~ user = model.User.get(username)
        #~
        #~ if user is not None:
            #~ identity['user'] = user
