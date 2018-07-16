# -*- coding: utf-8 -*-
import unittest as ut
from theme import theme

class Tests(ut.TestCase):
    def test_color(self):
        self.assertEqual(4, len(theme.color.correct2))

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
