from medienverwaltungweb.tests import *

class TestAmazonController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='amazon', action='index'))
        # Test response...
