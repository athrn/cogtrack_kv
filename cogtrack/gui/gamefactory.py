# -*- coding: utf-8 -*-
import tools

from cogtrack.gui.nbackwidget import NBackWidget
from cogtrack.game.nbackgame import NBackGame, random_chars

""" Connect games to game widgets """

def make_nback(n_back=2,
               max_rounds=20,
               show_symbol_interval=1,
               next_symbol_interval=3,
               symbols=r'ABCDEFGHI'):

    widget = NBackWidget()
    game = NBackGame(show_symbol=widget.show_symbol,
                     show_score=widget.show_score,
                     schedule=tools.schedule,
                     n_back=n_back,
                     max_rounds=max_rounds,
                     show_symbol_interval=show_symbol_interval,
                     next_symbol_interval=next_symbol_interval,
                     char_generator=random_chars(chars=symbols),
                     )

    
    widget.on_match = game.user_match
    widget.on_no_match = game.user_no_match

    return game, widget



games={'nback': make_nback}

def game_factory(game_type, game_settings):
    return games[game_type](**game_settings)
    

if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_gamefactory', failfast=True, exit=False)

    from gamefactorydemo import run
    run()
    
