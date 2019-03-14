# -*- coding: utf-8 -*-
import unittest as ut
from testing import start_app, press, Counter
import tools
from nback import NBack

from pprint import pprint

class DummyGame(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

        self.match = 0
        self.no_match = 0

    def update_score(self):
        self.show_score(self.match, self.match+1, self.no_match, self.no_match+1, self.match+self.no_match)
        
    def on_match(self):
        self.match += 1
        self.show_symbol('M')
        self.update_score()

    def on_no_match(self):
        self.no_match += 1
        self.show_symbol('N')
        self.update_score()

    def start(self):
        self.show_symbol('S')

    def stop(self):
        self.show_symbol('X')

    def cancel(self):
        self.show_symbol('C')
        

class Tests(ut.TestCase):

    def test1_buttons(self):
        count = Counter()
        nback = NBack()
        nback.set_callbacks(on_match=count.make('on_match'),
                            on_no_match=count.make('on_no_match'),
                            )
        press(nback.ids.match_button)
        press(nback.ids.match_button)
        press(nback.ids.match_button)
        press(nback.ids.no_match_button)
        press(nback.ids.no_match_button)

        self.assertEqual(3, count['on_match'])
        self.assertEqual(2, count['on_no_match'])

    def test1_set_score(self):
        nback = NBack()
        nback.show_score(1,2,3,4,5)
        btns = nback.ids.score_bar.ids
        self.assertEqual("1", btns.correct_match.text)
        self.assertEqual("2", btns.correct_no_match.text)
        self.assertEqual("3", btns.wrong_match.text)
        self.assertEqual("4", btns.wrong_no_match.text)
        self.assertEqual("5", btns.no_response.text)

        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
