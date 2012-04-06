import logging
import amazonproduct
import urllib
from StringIO import StringIO
from datetime import datetime
from pylons import config

import medienverwaltungweb.model as model
import medienverwaltungweb.lib.helpers as h
from medienverwaltungweb.model import meta
from medienverwaltungcommon.amazon import add_persons

log = logging.getLogger(__name__)

def AddMediumByISBN(isbn, search_index):
    """
        id_type: ISBN,
        search_index: Books, DVD
    """
    response = {'input_isbn':isbn}
    try:
        api = amazonproduct.API(config['Amazon.AccessKeyID'],
                                config['Amazon.SecretAccessKey'],
                                config['Amazon.Locale'],
                                config['Amazon.AssociateTag'])

        #~ log.debug("FOLLOW ME FOLLOW ME FOLLOW ME")
        #~ # Valid Values: SKU | UPC | EAN | ISBN (US only, when search
        #~ # index is Books) | JAN. UPC is not valid in the CA locale
        #~ id_type = 'SKU'
        #~ log.debug("id_type: %s" % id_type)

        #~ search_index = 'DVD'
        if search_index == 'Books':
            id_type = 'ISBN'
        elif search_index == 'DVD':
            id_type = 'EAN'
        else:
            raise Exception("unknown search_index: '%s'" % search_index)

        node = api.item_lookup(isbn,
                               IdType=id_type,
                               SearchIndex=search_index,
                                ResponseGroup="Images,ItemAttributes")
        item = node.Items.Item
        title = unicode(item.ItemAttributes.Title)
        response['title'] = title
        log.info("title: %s" % title)

        media_type = meta.Session\
                         .query(model.MediaType)\
                         .filter(model.MediaType.name == 'book')\
                         .first()

        medium = model.Medium()
        medium.title = title
        medium.created_ts = datetime.now()
        medium.updated_ts = datetime.now()
        log.debug("medium.title: %s" % medium.title)
        medium.media_type_id = media_type.id
        medium.isbn = isbn

        try:
            url = str(item.LargeImage.URL)
        except:
            url = None
            log.warn("%s has no image" % medium)

        if url:
            print url
            webFile = urllib.urlopen(url)
            buffer = StringIO()
            buffer.write(webFile.read())
            if buffer.len > 65536:
                log.warn("image is too big")
            else:
                medium.image_data = buffer
        else:
            url = ""

        response['image_url'] = url

        meta.Session.add(medium)
        #~ session.commit()

        asin = model.MediaToAsin()
        asin.media_id = medium.id
        asin.asin = item.ASIN
        #~ session.add(asin)
        medium.asins.append(asin)

        added_persons = []
        add_persons(item, 'Author', medium, added_persons, meta.Session)
        add_persons(item, 'Creator', medium, added_persons, meta.Session)
        add_persons(item, 'Manufacturer', medium, added_persons, meta.Session)

        response['persons'] = map(lambda x: x.name, added_persons)

        meta.Session.commit()

        response['medium_url'] = h.url_for(controller='medium', action='edit', id=medium.id)
        response['success'] = True
        response['medium_id'] = medium.id
        response['message'] = "Successfully added '%s'" % isbn
    except Exception, ex:
        log.error("AddMediumByISBN: %s" % ex)
        response['success'] = False
        response['message'] = str(ex)

    log.debug("response: %s" % response)
    return response
    log.info("added: %s" % ", ".join(map(lambda x: x.name, added_persons)))

def GetTmpMediumByISBN(isbn, search_index):
    """
        id_type: ISBN,
        search_index: Books, DVD
    """
    response = {'isbn':isbn}
    api = amazonproduct.API(config['Amazon.AccessKeyID'],
                            config['Amazon.SecretAccessKey'])

    #~ # Valid Values: SKU | UPC | EAN | ISBN (US only, when search
    #~ # index is Books) | JAN. UPC is not valid in the CA locale
    #~ id_type = 'SKU'
    #~ log.debug("id_type: %s" % id_type)

    #~ search_index = 'DVD'
    if search_index == 'Books':
        id_type = 'ISBN'
    elif search_index == 'DVD':
        id_type = 'EAN'
    else:
        raise Exception("unknown search_index: '%s'" % search_index)

    node = api.item_lookup(isbn,
                           IdType=id_type,
                           SearchIndex=search_index,
                           ResponseGroup="Images,ItemAttributes")
    item = node.Items.Item
    response['title'] = unicode(item.ItemAttributes.Title)
    try:
        #~ response['image_url'] = str(item.LargeImage.URL)
        response['image_url'] = str(item.MediumImage.URL)
    except:
        response['image_url'] = None
        log.warn("%s has no image" % medium)

    response['persons'] = {'Author':['John Doe', 'Some One'],
                           'Creator':['Foo Corp.']}

    response['persons'] = {}
    add_persons_response(item, 'Author', response['persons'])
    add_persons_response(item, 'Creator', response['persons'])
    add_persons_response(item, 'Manufacturer', response['persons'])
    return response

def add_persons_response(item, relation_name, persons):
    if not relation_name in item.ItemAttributes.__dict__:
        log.warn("asin %s has no '%s'" % (item.ASIN, relation_name))
        return

    persons[relation_name] = []
    for subitem in item.ItemAttributes.__dict__[relation_name]:
        subitem = unicode(subitem)
        log.debug("amazon person: %s" % subitem)
        persons[relation_name].append(subitem)
