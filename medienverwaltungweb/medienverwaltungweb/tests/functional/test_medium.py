from pprint import pprint, pformat
from medienverwaltungweb.tests import *

class TestMediumController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='medium', action='index'))

    def test_mass_add(self):
        response = self.app.get(url(controller='medium', action='mass_add'))
        assert '<h1>Add Media</h1>' in response

    def test_list(self):
        response = self.app.get(url(controller='medium', action='list'))

    def test_list_gallery(self):
        response = self.app.get(url(controller='medium', action='list_gallery'))

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
        #~ self.assertEqual('http://localhost/medium/edit', response.location)
        #~ assert 'http://localhost/medium/edit' == response.location

        response2 = self.app.get(response.location)
        assert 'Foo' in response2
        #~ assert 'added medium Foo3' in response2
