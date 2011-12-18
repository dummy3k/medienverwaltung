from medienverwaltungweb.tests import *

class TestJsonapiController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='JsonApi', action='index'))
        # Test response...
