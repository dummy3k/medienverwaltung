import logging
import Image, ImageFile
from StringIO import StringIO
from datetime import datetime

from sqlalchemy import *
import meta
import tag

log = logging.getLogger(__name__)

media_table = Table('media', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(100)),
    Column('image_data', PickleType(mutable=False)),
    Column('media_type_id', Integer, ForeignKey('media_types.id')),
    Column('isbn', String(15)),
    Column('created_ts', DateTime),
    Column('updated_ts', DateTime),
    Column('image_crop', PickleType(mutable=False)),
)

def __shrink__(original_buffer):
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
        log.info("reduced image size by %d%%" % (percent * 100,))
        
    return smaller_buffer

class Medium(object):
    def __unicode__(self):
        return "<Medium(%s, '%s')>" % (self.id, self.title)

    #~ __str__ = __unicode__

    def __repr__(self):
        return self.__unicode__().encode('ascii', 'replace')

    def get_tagstring(self):
        retval = ""
        for item in self.tags:
            if len(retval) > 0:
                retval += " "

            retval += item.name

        return retval

    def set_tagstring(self, s):
        tag_names = map(lambda x: x.name, self.tags)
        for item in s.split(' '):
            if item:
                if not item in tag_names:
                    mytag = tag.Tag()
                    mytag.name = item
                    self.tags.append(mytag)
                else:
                    tag_names.remove(item)

        for item in tag_names:
            for tagobj in self.tags:
                if tagobj.name == item:
                    self.tags.remove(tagobj)
                    break


    def set_image_buffer(self, buffer):
        self.image_data = __shrink__(buffer)
        if self.image_data.len >= 65536:
            raise Exception("image to big")
            
        self.image_crop = None
        self.updated_ts = datetime.now()
