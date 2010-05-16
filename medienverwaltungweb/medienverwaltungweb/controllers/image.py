import logging
import Image, ImageFile
from StringIO import StringIO

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, etag_cache

from medienverwaltungweb.lib.base import BaseController, render
from medienverwaltungweb.model import meta
import medienverwaltungweb.model as model

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

