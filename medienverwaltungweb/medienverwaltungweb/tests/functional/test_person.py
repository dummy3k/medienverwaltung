from medienverwaltungweb.tests import *
from medienverwaltungweb.tests.functional import *
log = logging.getLogger(__name__)

class TestPersonController(TestController):
    def setUp(self):
        TestController.setUp(self)

        self.bruce = model.Person()
        self.bruce.name = u"Bruce Schneier"
        meta.Session.add(self.bruce)

        self.medium = model.Medium()
        self.medium.title = u"A Medium"
        meta.Session.add(self.medium)

        self.relation = model.RelationType()
        self.relation.name = u"Author"
        meta.Session.add(self.relation)

        meta.Session.commit()

        self.assertEqual(1, self.bruce.id)

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

    def test_edit_post_alias(self):
        response = self.app.get(url(controller='person',
                                    action='edit_post',
                                    id='1'),
                                 params={'name':'Changed',
                                         'create_alias':'yes'})

        record = meta.Session.query(model.Person).get(1)
        self.assertEqual('Changed', record.name)
        self.assertEqual(1, len(record.aliases))

    def test_list(self):
        record = model.Person()
        record.name = u"Chuck Norries"
        meta.Session.add(record)
        meta.Session.commit()

        response = self.app.get(url(controller='person',
                                    action='list'))

        assert "Bruce Schneier" in response
        assert "Chuck Norries" in response

    def test_top_ten(self):
        record = model.PersonToMedia()
        self.bruce.persons_to_media.append(record)
        self.medium.persons_to_media.append(record)
        self.relation.persons_to_media.append(record)
        meta.Session.add(record)

        meta.Session.commit()

        response = self.app.get(url(controller='person',
                                    action='top_ten'))

        assert "Bruce Schneier" in response
        assert "Author" in response
        assert not "Actor" in response

    def test_add_to_medium_post(self):
        response = self.app.get(url(controller='person',
                                    action='add_to_medium_post',
                                    id='1'),
                                 params={'name':'Foo',
                                         'role':'Author'})

        record = meta.Session.query(model.Person).get(2)
        self.assertNotEqual(None, record)
        self.assertEqual('Foo', record.name)
        self.assertEqual('A Medium', record.persons_to_media[0].medium.title)

    def test_merge_post(self):
        record = model.PersonToMedia()
        self.bruce.persons_to_media.append(record)
        self.medium.persons_to_media.append(record)
        self.relation.persons_to_media.append(record)
        meta.Session.add(record)

        john = model.Person()
        john.name = u"John"
        meta.Session.add(john)

        record = model.PersonToMedia()
        john.persons_to_media.append(record)
        self.medium.persons_to_media.append(record)
        self.relation.persons_to_media.append(record)
        meta.Session.add(record)

        meta.Session.commit()

        response = self.app.get(url(controller='person',
                                    action='merge_post'),
                                 params={'primary_id':'2',
                                         'person_ids_str':'1,2'})

        #~ record = meta.Session.query(model.PersonToMedia).get(1)
        #~ self.assertEqual(None, record)

    def test_remove_from_media(self):
        record = model.PersonToMedia()
        self.bruce.persons_to_media.append(record)
        self.medium.persons_to_media.append(record)
        self.relation.persons_to_media.append(record)
        meta.Session.add(record)
        meta.Session.commit()

        response = self.app.get(url(controller='person',
                                    action='remove_from_media',
                                    id='1'),
                                 params={'name':'Foo',
                                         'role':'Author'})

        record = meta.Session.query(model.PersonToMedia).get(1)
        self.assertEqual(None, record)
