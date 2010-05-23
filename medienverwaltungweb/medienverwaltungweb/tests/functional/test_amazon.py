from medienverwaltungweb.tests import *
from medienverwaltungweb.tests.functional import *
log = logging.getLogger(__name__)

class TestAmazonController(TestController):
    def setUp(self):
        TestController.setUp(self)

        self.medium = model.Medium()
        self.medium.title = u"Some Medium"
        self.medium.media_type_id = 2
        meta.Session.add(self.medium)
        #~ meta.Session.commit()


    def test_index(self):
        response = self.app.get(url(controller='amazon', action='index'))

    def test_remove_asin(self):
        record = model.MediaToAsin()
        record.media_id = 1
        record.asin = "A12345"
        self.medium.asins.append(record)

        self.assertNotEqual(None, meta.Session.query(model.MediaToAsin).get(1))
        response = self.app.get(url(controller='amazon',
								    action='remove_asin',
								    id=1,
								    asin='A12345'))
        self.assertEqual(None, meta.Session.query(model.MediaToAsin).get(1))

    def test_clear_persons(self):
        person = model.Person()
        person.name = "Foo"

        record = model.PersonToMedia()
        record.media_id = 1
        record.asin = "A12345"
        person.persons_to_media.append(record)
        self.medium.persons_to_media.append(record)

        self.assertNotEqual(None, meta.Session.query(model.PersonToMedia).get(1))
        response = self.app.get(url(controller='amazon',
								    action='clear_persons',
								    id=1))
        self.assertEqual(None, meta.Session.query(model.PersonToMedia).get(1))
