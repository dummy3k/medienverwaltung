import logging
import Image, ImageFile
import urllib
from StringIO import StringIO
from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons import url
from pylons.controllers.util import abort, redirect, etag_cache
from pylons.i18n import _, ungettext

import medienverwaltungweb.lib.helpers as h
import medienverwaltungweb.model as model
from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta

log = logging.getLogger(__name__)

class ImageController(BaseController):
    def thumbnail(self, id, width, height):
        item = meta.find(model.Medium, id)
        etag_cache(str(item.updated_ts))

        p = ImageFile.Parser()
        p.feed(item.image_data.getvalue())
        img = p.close()

        if item.image_crop:
            img = img.crop(item.image_crop)

        #~ log.debug("size: %s, %s" % (width, height))
        size = int(width), int(height)
        img.thumbnail(size)
        #~ log.debug("imgsize: %s, %s" % img.size)

        buffer = StringIO()
        img.save(buffer, format='png')
        response.content_type = 'image/png'

        return buffer.getvalue()

    def upload(self, id):
        c.id = id
        return render('image/upload.mako')
        
    def upload_post(self, id):
        myfile = request.POST['myfile']

        buffer = StringIO()
        buffer.write(myfile.file.read())

        record = meta.Session.query(model.Medium).get(id)
        record.set_image_buffer(buffer)
        
        meta.Session.add(record)
        meta.Session.commit()
        
        h.flash(_("added image (%d bytes)") % buffer.len)
        return redirect(url(controller='medium', action='edit', id=id))
        
    def download_post(self, id):
        image_url = request.params.get('url')
        webFile = urllib.urlopen(image_url)
        buffer = StringIO()
        buffer.write(webFile.read())

        record = meta.Session.query(model.Medium).get(id)
        record.set_image_buffer(buffer)
        meta.Session.add(record)
        meta.Session.commit()
        
        h.flash(_("added image (%d bytes)") % buffer.len)
        return redirect(url(controller='medium', action='edit', id=id))
        
    def raw_image(self, id):
        item = meta.find(model.Medium, id)

        p = ImageFile.Parser()
        p.feed(item.image_data.getvalue())
        img = p.close()

        buffer = StringIO()
        img.save(buffer, format='png')
        response.content_type = 'image/png'

        etag_cache(str(item.updated_ts))
        return buffer.getvalue()

    def crop_image(self, id):
        c.item = meta.find(model.Medium, id)
        return render('image/crop_image.mako')

    def crop_image_post(self, id):
        crop = (int(request.params.get('x')),
                int(request.params.get('y')),
                int(request.params.get('x2')),
                int(request.params.get('y2')))

        item = meta.find(model.Medium, id)
        item.image_crop = crop
        item.updated_ts = datetime.now()
        meta.Session.add(item)
        meta.Session.commit()
        h.flash(_("updated: '%s'") % h.html_escape(item.title))

        return_to = request.params.get('return_to')
        log.debug("return_to: %s" % return_to)
        if return_to:
            return redirect(str(return_to))
        else:
            return redirect(url(controller='medium', action='edit', id=id))

