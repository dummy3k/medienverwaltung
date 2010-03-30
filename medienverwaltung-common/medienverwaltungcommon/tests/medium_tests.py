import unittest
import math

from medienverwaltungcommon import model

class TestTracerouteParser(unittest.TestCase):
    def testSetOne(self):
        m = model.Medium()
        m.set_tagstring('foo')
        self.assertEqual(len(m.tags), 1)
        self.assertEqual(m.tags[0].name, 'foo')
        self.assertEqual(m.get_tagstring(), 'foo')

    def testSetTwo(self):
        m = model.Medium()
        m.set_tagstring('foo bar')
        self.assertEqual(len(m.tags), 2)
        self.assertEqual(m.get_tagstring(), 'foo bar')
        self.assertEqual(m.tags[0].name, 'foo')
        self.assertEqual(m.tags[1].name, 'bar')

    def testSetOneTwice(self):
        m = model.Medium()
        m.set_tagstring('foo')
        m.set_tagstring('foo')
        self.assertEqual(len(m.tags), 1)
        self.assertEqual(m.tags[0].name, 'foo')
        self.assertEqual(m.get_tagstring(), 'foo')

    def testSetSomeNewSomeNot(self):
        m = model.Medium()
        m.set_tagstring('foo bar')
        m.set_tagstring('foo test')
        self.assertEqual(len(m.tags), 3)
        self.assertEqual(m.tags[0].name, 'foo')
        self.assertEqual(m.tags[1].name, 'bar')
        self.assertEqual(m.tags[2].name, 'test')
        self.assertEqual(m.get_tagstring(), 'foo bar test')


if __name__ == '__main__':
    unittest.main()
