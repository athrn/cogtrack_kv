# -*- coding: utf-8 -*-
import unittest as ut
from kivy.app import App
from kivy.uix.label import Label

from testing import start_widget
from tools import * 

def print_stuff():
    print("This was called")

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

    # def test_schedule(self):
    #     # REVIEW: Does not work as test...
    #     label = Label(text='Old Text')
    #     start_widget(label)

    #     def set_label_text(t):
    #         label.text = 'New Text'
    #         print("Setting")
        
    #     schedule(0.01, set_label_text)
    #     Clock.usleep(1e5)

    #     print(label.text)
        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
