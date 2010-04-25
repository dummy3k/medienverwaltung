from medienverwaltungweb.tests import *
from medienverwaltungweb.tests.functional import *
log = logging.getLogger(__name__)

class TestSearchController(TestController):
    def setUp(self):
        TestController.setUp(self)

        record = model.Medium()
        record.title = u"FindMe"
        record.image_data = "foo"
        record.isbn = 'isbn1234'
        record.media_type_id = 2
        meta.Session.add(record)
        meta.Session.commit()

        meta.Session.commit()

    def test_index(self):
        response = self.app.get(url(controller='search', action='index'))

    def test_search_post(self):
        response = self.app.get(url(controller='search',
                                    action='search_post'),
                                 params={'query':'find'})

        assert "FindMe" in response
