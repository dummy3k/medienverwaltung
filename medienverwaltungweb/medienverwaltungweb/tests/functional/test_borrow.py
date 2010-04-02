from medienverwaltungweb.tests import *

class TestBorrowController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='borrow', action='index'))
        # Test response...
