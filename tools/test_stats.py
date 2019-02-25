import unittest as ut
from math import sqrt

from stats import *

class Tests(ut.TestCase):
    def test(self):
        s = Stats()
        s.add(1)
        s.add(2)
        s += (1)
        s.add(2)

        self.assertEqual(4, s.count)
        self.assertEqual(6, s.sum)
        self.assertEqual(1.5, s.avg)
        self.assertEqual(0.5, s.stdev)

        self.assertEqual("N:4 Sum:6 Avg:1.5 Stdev:0.5", str(s))

    # TODO: Consider removing + operator support. May be confusing. s + 1 + (2 + 3) 
    def test_repeated_plus(self):
        s = Stats()
        # NOTE: left add only. 1 + 2 + s would be error prone.
        s = s + 1 + 2 + 3

        self.assertEqual(3, s.count)
        self.assertEqual(6, s.sum)
        self.assertEqual(2.0, s.avg)
        self.assertAlmostEqual(sqrt(2./3), s.stdev)

    def test_repeated_add(self):
        s = Stats()
        s = s.add(1).add(2)

        self.assertEqual(2, s.count)
        self.assertEqual(3, s.sum)
        self.assertEqual(1.5, s.avg)
        self.assertAlmostEqual(sqrt(2*0.25/2), s.stdev)
        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
    
