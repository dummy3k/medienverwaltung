from medienverwaltungweb.tests import *
from medienverwaltungweb.tests.functional import *
log = logging.getLogger(__name__)

class TestPersonController(TestController):
    def setUp(self):
        TestController.setUp(self)

        record = model.Person()
        record.name = u"Bruce Schneier"
        meta.Session.add(record)
        meta.Session.commit()

        self.assertEqual(1, record.id)

    def test_edit(self):
        response = self.app.get(url(controller='person',
                                    action='edit',
                                    id=1))

        assert "Bruce Schneier" in response

    def test_edit_post(self):
        response = self.app.get(url(controller='person',
                                    action='edit_post',
                                    id='1'),
                                 params={'name':'Changed'})

        record = meta.Session.query(model.Person).get(1)
        self.assertEqual('Changed', record.name)


    def test_list(self):
        record = model.Person()
        record.name = u"Chuck Norries"
        meta.Session.add(record)
        meta.Session.commit()

        response = self.app.get(url(controller='person',
                                    action='list'))

        assert "Bruce Schneier" in response
        assert "Chuck Norries" in response

