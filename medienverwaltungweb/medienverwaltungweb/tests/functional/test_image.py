from medienverwaltungweb.tests import *
from medienverwaltungweb.tests.functional import *

class TestImageController(TestController):
    def setUp(self):
        #~ log.debug("FOLLOW ME: setUp")
        TestController.setUp(self)

        record = model.Medium()
        record.title = u"Second_Medium"
        record.image_data = "foo"
        #~ record.created_ts = datetime.now()
        #~ record.updated_ts = datetime.now()
        record.media_type_id = 2
        meta.Session.add(record)

    def test_crop_image(self):
        response = self.app.get(url(controller='image',
                                    action='crop_image',
                                    id='1'))

        print response
        assert "Crop Medium" in response

    def test_crop_image_post(self):
        response = self.app.post(url(controller='image',
                                     action='crop_image_post',
                                     id='1'),
                                 params={'x':'1',
                                         'y':'2',
                                         'x2':'3',
                                         'y2':'4'})

        print response
        record = meta.Session.query(model.Medium).get(1)
        self.assertEqual( (1,2,3,4) , record.image_crop)

