# -*- coding: utf-8 -*-

from imaincontroller import IMainController

from cogtrack.game import game

class MainController(IMainController):

    def __init__(self, gui, game_factory):
        self.game_factory = game_factory
        self.games = {}
        self.gui = gui
        # Set self as controller in gui object
        self.gui.controller = self

    def start(self):
        self.show_select_game()

    def add_game(self, game_name, game_type, game_settings):
        self.games[game_name] = (game_type, game_settings)

    def start_game(self, game_name):
        (game_type, game_settings) = self.games[game_name]
        self.current_game, game_widget = self.game_factory(game_type, game_settings)

        # NOTE: The game may stop either by itself or by the user pressing the stop button.
        # self.current_game.on_stop = self.show_score
        # self.current_game.on_cancel = self.show_select_game

        self.current_game.on_game_over = self.stop_game

        self.gui.show_game(game_widget)
        self.current_game.start()

    def show_score(self):
        self.gui.show_score(self.current_game.get_score())

    def stop_game(self):
        self.current_game.stop()
        self.show_score()

    def cancel_game(self):
        self.current_game.cancel()
        self.show_select_game()

    def save_score(self):
        # TODO: save_score
        self.show_select_game()
            
    def show_select_game(self):
        self.current_game = None
        self.gui.show_select_game()


    def list_games(self):
        return self.games.keys()



   
if __name__ == "__main__":
    import unittest as ut
    MainController(None, None)
    # ut.main(module='test_x', failfast=True, exit=False)

