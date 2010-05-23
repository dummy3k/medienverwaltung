from medienverwaltungweb.tests import *
from medienverwaltungweb.tests.functional import *
from pylons import config, url
log = logging.getLogger(__name__)

class TestMediumController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='medium', action='index'))

    def test_mass_add(self):
        response = self.app.get(url(controller='medium', action='mass_add'))
        assert '<h1>Add Media</h1>' in response

    def test_mass_add_post_no_name(self):
        response = self.app.get(url(controller='medium', action='mass_add_post'))
        assert 'http://localhost/medium/mass_add' == response.location

        response2 = self.app.get(response.location)
        assert 'please specify name' in response2

    def test_mass_add_post_no_type(self):
        response = self.app.get(url(controller='medium',
                                    action='mass_add_post',
                                    title="Foo"))
        assert 'http://localhost/medium/mass_add' == response.location

        response2 = self.app.get(response.location)
        assert 'please specify media type' in response2

    def test_mass_add_post(self):
        response = self.app.get(url(controller='medium',
                                    action='mass_add_post',
                                    title="Foo3",
                                    media_type="1"))
        self.assertEqual('http://localhost/medium/edit/1', response.location)

        response2 = self.app.get(response.location)
        print response2
        assert 'Foo' in response2
        assert 'added medium' in response2

    def test_mass_add_post_blank_lines(self):
        response = self.app.get(url(controller='medium',
                                    action='mass_add_post',
                                    title="Foo3\n",
                                    media_type="1"))
        self.assertEqual('http://localhost/medium/edit/1', response.location)

        response2 = self.app.get(response.location)
        print response2
        assert 'Foo' in response2
        assert 'added medium' in response2

    def test_mass_add_post_double(self):
        response = self.app.get(url(controller='medium',
                                    action='mass_add_post',
                                    title="Foo3",
                                    media_type="1"))

        response = self.app.get(url(controller='medium',
                                    action='mass_add_post',
                                    title="Foo3",
                                    media_type="1"))
        response2 = self.app.get(response.location)
        #~ print response
        assert 'medium already exists:' in response2

    def test_list_gallery(self):
        response = self.app.get(url(controller='medium', action='list_gallery'))

class TestMediumControllerWithData(TestController):
    def setUp(self):
        #~ log.debug("FOLLOW ME: setUp")
        TestController.setUp(self)

        response = self.app.get(url(controller='medium',
                                    action='mass_add_post',
                                    title="A_Media_Title",
                                    media_type="1"))

        record = model.Medium()
        record.title = u"Second_Medium"
        record.image_data = "foo"
        #~ record.created_ts = datetime.now()
        #~ record.updated_ts = datetime.now()
        record.media_type_id = 2
        meta.Session.add(record)

    def test_index(self):
        response = self.app.get(url(controller='medium', action='index'))
        self.check_list(response)

    def test_list(self):
        response = self.app.get(url(controller='medium', action='list'))
        self.check_list(response)

    def test_list_tagged(self):
        record = model.Tag()
        record.name = u"MyTag"
        
        medium = meta.Session.query(model.Medium).get(1)
        medium.tags.append(record)

        response = self.app.get(url(controller='medium',
                                    action='list',
                                    tag='MyTag'))

        assert 'A_Media_Title' in response
        assert 'Second_Medium' not in response

    def test_list_typed(self):
        response = self.app.get(url(controller='medium',
                                    action='list',
                                    type='books'))

        assert 'A_Media_Title' in response
        #~ assert 'Second_Medium' in response

    def test_new_media_rss(self):
        config['base_url'] = ''
        response = self.app.get(url(controller='medium',
                                    action='new_media_rss'))

        assert 'A_Media_Title' in response
        assert 'Second_Medium' in response

    def check_list(self, response):
        assert 'All Media List' in response
        assert 'A_Media_Title' in response
        assert 'Second_Medium' in response

    def test_index_id(self):
        response = self.app.get(url(controller='medium',
                                action='index',
                                id="1"))
        self.check_edit(response)

    def test_edit(self):
        response = self.app.get(url(controller='medium',
                                action='edit',
                                id="1"))
        self.check_edit(response)

    def check_edit(self, response):
        assert 'Edit Medium' in response
        assert 'A_Media_Title' in response

    def test_list_no_image(self):
        response = self.app.get(url(controller='medium', action='list_no_image'))
        assert 'A_Media_Title' in response
        assert 'Second_Medium' not in response

    def test_query(self):
        self.assertNotEqual(None, meta.Session.query(model.Medium).get(2))

    def test_delete_many(self):
        response = self.app.get(url(controller='medium',
                                    action='delete_many',
                                    item_id_1='1'))
        self.assertEqual(None, meta.Session.query(model.Medium).get(1))
        self.assertNotEqual(None, meta.Session.query(model.Medium).get(2))

    def test_delete_one(self):
        response = self.app.get(url(controller='medium',
                                    action='delete_one',
                                    id='2'))
        self.assertEqual(None, meta.Session.query(model.Medium).get(2))
        self.assertNotEqual(None, meta.Session.query(model.Medium).get(1))

    def test_edit_post(self):
        response = self.app.post(url(controller='medium',
                                     action='edit_post'),
                                 params={'id':'2',
                                         'title':'Other title',
                                         'tags':''})

        record = meta.Session.query(model.Medium).get(2)
        self.assertEqual('Other title', record.title)

    def test_next_without_image(self):
        response = self.app.get(url(controller='medium',
                                    action='next_without_image',
                                    id='2'))

        self.assertEqual('http://localhost/medium/edit/1', response.location)

    def test_crop_image(self):
        response = self.app.get(url(controller='medium',
                                    action='crop_image',
                                    id='2'))

        print response
        assert "Crop Medium" in response

    def test_crop_image_post(self):
        response = self.app.post(url(controller='medium',
                                     action='crop_image_post',
                                     id='2'),
                                 params={'x':'1',
                                         'y':'2',
                                         'x2':'3',
                                         'y2':'4'})

        print response
        record = meta.Session.query(model.Medium).get(2)
        self.assertEqual( (1,2,3,4) , record.image_crop)

    def test_set_view_options(self):
        response = self.app.post(url(controller='medium',
                                     action='set_view_options'),
                                 params={'items_per_page':'123'})

        self.assertEqual( 123 , response.session['items_per_page'])

if __name__ == '__main__':
    unittest.main()
