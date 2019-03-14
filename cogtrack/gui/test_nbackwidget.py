# -*- coding: utf-8 -*-
import unittest as ut
from testing import start_app, press, Counter
import tools
from nbackwidget import NBackWidget

from pprint import pprint
        

class Tests(ut.TestCase):

    def test1_buttons(self):
        count = Counter()
        nback = NBackWidget()
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
        nback = NBackWidget()
        nback.show_score(1,2,3,4,5)
        btns = nback.ids.score_bar.ids
        self.assertEqual("1", btns.correct_match.text)
        self.assertEqual("2", btns.correct_no_match.text)
        self.assertEqual("3", btns.wrong_match.text)
        self.assertEqual("4", btns.wrong_no_match.text)
        self.assertEqual("5", btns.no_response.text)

        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
