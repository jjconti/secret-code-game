import unittest
from secrets import *

class TestEq(unittest.TestCase):
    '''Test __eq__ method for Row and Colour classes'''

    def setUp(self):
        pass

    def testc1(self):
        c1 = Colour(0, 0, False)
        c2 = Colour(0, 0, False)
        self.assertTrue(c1 == c2)

    def testc2(self):
        c1 = Colour(0, 0, False)
        c1.next()
        c2 = Colour(0, 0, False)
        c2.next()
        self.assertTrue(c1 == c2)

    def testc3(self):
        c1 = Colour(0, 0, False)
        c2 = Colour(0, 0, False)
        c2.next()
        self.assertFalse(c1 == c2)

    def testc4(self):
        c1 = Colour(0, 0, False)
        c1.next(4)
        c2 = Colour(0, 0, False)
        c2.next(4)
        self.assertTrue(c1 == c2)

    def testc5(self):
        c1 = Colour(0, 0, False)
        c1.next(13)
        c2 = Colour(0, 0, False)
        c2.next(13)
        self.assertTrue(c1 == c2)

    #def testr1(self):
    #    r1 = Row(0, 0, False)
    #    r2 = Row(0, 0, False)
    #    self.assertTrue(r1 == r2)

if __name__ == '__main__':
    unittest.main()
