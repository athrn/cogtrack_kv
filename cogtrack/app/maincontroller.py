# -*- coding: utf-8 -*-

from cogtrack.game import game

class MainController(object):

    def __init__(self, gui, game_factory):
        self.game_factory = game_factory
        self.games = {}
        self.gui = gui
        # Set self as controller in gui object
        self.gui.controller = self

    def start(self):
        self._show_select_game()

    def add_game(self, game_name, game_type, game_settings):
        self.games[game_name] = (game_type, game_settings)

    def start_game(self, game_name):
        (game_type, game_settings) = self.games[game_name]
        self.current_game, game_widget = self.game_factory(game_type, game_settings)

        # NOTE: The game may call on_game_over when it is finished.
        self.current_game.on_game_over = self.stop_game

        self.gui.show_game(game_widget)
        self.current_game.start()

    def _show_score(self):
        self.gui.show_score(self.current_game.get_score())

    def stop_game(self):
        self.current_game.stop()
        self._show_score()

    def cancel_game(self):
        self.current_game.cancel()
        self._show_select_game()

    def save_score(self):
        # TODO: save_score
        self._show_select_game()

    def discard_score(self):
        self._show_select_game()

    def _show_select_game(self):
        self.current_game = None
        self.gui.show_select_game()


    def list_games(self):
        return self.games.keys()



   
if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_maincontroller', failfast=True, exit=False)

