from unittest import TestCase

import medienverwaltungweb.lib.helpers as h

class TestPersonController(TestCase):
    def testIff(self):
        self.assertEqual('true', h.iif(1==1, 'true', 'false'))
        self.assertEqual('false', h.iif(1==2, 'true', 'false'))

    def testFind(self):
        self.assertEqual(1, h.find(range(10), lambda x: x==1))
