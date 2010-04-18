if __name__ == '__main__':
    import logging.config
    logging.config.fileConfig("settings.conf")

import logging
import xmlrpclib
from optfunc import optfunc
from pprint import pprint, pformat

log = logging.getLogger(__name__)
isbn_log = logging.getLogger('isbn')

def one(url, isbn):
    print "ISBN: %s" % isbn
    isbn_log.info("ISBN: %s" % isbn)

    service_url = "%s/api/index" % url
    server = xmlrpclib.Server(service_url)
    result = server.AddMediumByISBN(isbn)
    log.debug("result:\n%s" % pformat(result))
    if not result['success']:
        print "Failure: %s" % result['message']
    else:
        print "Success!"
        print "\tTitle:\t\t%s" % result['title']
        print "\tPersons:\t%s" % ", ".join(result['persons'])
        print "\tLink:\t\t%s%s" % (url, result['medium_url'])
        print "\tImage:\t\t%s" % result['image_url']

    return result['success']

def for_ever():
    while True:
        try:
            user_input = raw_input("ISBN:")
        except KeyboardInterrupt:
            print "\nbye..."
            break
            
        print user_input
        if user_input == 'exit':
            break

        if not user_input:
            continue

        if one(user_input):
            os.system('play -q audio/success.wav')
        else:
            os.system('play -q audio/failure.wav')

if __name__ == '__main__':
    #~ optfunc.run(find)
    optfunc.main([for_ever,one])
