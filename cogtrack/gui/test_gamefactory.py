# -*- coding: utf-8 -*-
import unittest as ut
from gamefactory import game_factory

from testing import press
import tools

class Tests(ut.TestCase):

    def test1_nback(self):
        g,w = game_factory(game_type='nback',
                           game_settings=dict(n_back=2,
                                              max_rounds=5,
                                              show_symbol_interval=1,
                                              next_symbol_interval=3))

        
        g.start()
        self.assertEqual(tools.schedule, g.schedule)
        ids = w.ids.score_bar.ids
        self.assertEqual(0, ids.correct_match.score)
        press(w.ids.match_button)
        press(w.ids.no_match_button)

        # TODO: Not sure what to test yet.
        
        g.stop()
        g.cancel()



if __name__ == "__main__":
    ut.main(failfast=True, exit=False)




