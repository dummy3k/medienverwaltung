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
        return render('image/upload.mako')
        
    def upload_post(self, id):
        myfile = request.POST['myfile']

        buffer = StringIO()
        buffer.write(myfile.file.read())
        buffer = self.__shrink__(buffer)
        
        if buffer.len >= 65536:
            # 69198 defenitly fails. if the size is to blame.
            # i dont know :(
            h.flash(_("image is to big."))
            return redirect(url(controller='image', action='upload', id=id))
        
        record = meta.Session.query(model.Medium).get(id)
        record.image_data = buffer
        record.image_crop = None
        record.updated_ts = datetime.now()
        meta.Session.update(record)
        meta.Session.commit()
        
        h.flash(_("added image (%d bytes)") % buffer.len)
        return redirect(url(controller='medium', action='edit', id=id))
        
    def download_post(self, id):
        image_url = request.params.get('url')
        webFile = urllib.urlopen(image_url)
        buffer = StringIO()
        buffer.write(webFile.read())
        buffer = self.__shrink__(buffer)
        if buffer.len >= 65536:
            # 69198 defenitly fails. if the size is to blame.
            # i dont know :(
            h.flash(_("image is to big."))
            return redirect(url(controller='image', action='upload', id=id))
        
        record = meta.Session.query(model.Medium).get(id)
        record.image_data = buffer
        record.image_crop = None
        record.updated_ts = datetime.now()
        meta.Session.update(record)
        meta.Session.commit()
        
        h.flash(_("added image (%d bytes)") % buffer.len)
        return redirect(url(controller='medium', action='edit', id=id))
        
    def __shrink__(self, original_buffer):
        smaller_buffer = original_buffer
        percent = 1
        while smaller_buffer.len >= 65536:
            percent -= 0.1
            log.debug("percent: %s" % percent)
            if percent < 0.01:
                raise Exception("can't shrink image")
            
            p = ImageFile.Parser()
            p.feed(original_buffer.getvalue())
            img = p.close()

            log.debug("Before Size: %d,%d" % img.size)
            img.thumbnail((int(img.size[0] * percent),
                           int(img.size[1] * percent)))
            log.debug("After Size: %d,%d" % img.size)

            smaller_buffer = StringIO()
            img.save(smaller_buffer, format='png')
            log.debug("smaller_buffer size: %d" % smaller_buffer.len)

        if percent < 1:
            h.flash(_("reduced image size by %d%%") % (percent * 100,))
            
        return smaller_buffer
