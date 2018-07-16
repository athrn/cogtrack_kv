# -*- coding: utf-8 -*-
import unittest as ut

from tools import * 

class Tests(ut.TestCase):
    def test_namedproperties(self):
        x = NamedProperties(ape='Ape', bat='Bat')
        self.assertEqual('Ape', x.ape)
        self.assertEqual('Bat', x.bat)
        y = NamedProperties(cat='Cat', dog='Dog')
        self.assertEqual('Cat', y.cat)
        self.assertEqual('Dog', y.dog)
        self.assertRaises(AttributeError, getattr, y, 'ape')
        self.assertRaises(AttributeError, getattr, x, 'dog')
        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
