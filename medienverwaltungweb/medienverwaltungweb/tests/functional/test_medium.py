from medienverwaltungweb.tests import *

class TestMediumController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='medium', action='index'))
        # Test response...
