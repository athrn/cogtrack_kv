# -*- coding: utf-8 -*-

from imaincontroller import IMainController




class MainController(IMainController):

    def __init__(self, game_factory):
        self.game_factory = game_factory
        self.games = {}

    def add_game(self, game_name, game_type, settings):
        pass

    def start_game(self, game_name):
        return game

    def list_games(self):
        return []

    def save_score(self, game_name, score):
        pass


   
if __name__ == "__main__":
    import unittest as ut
    MainController(None)
    # ut.main(module='test_x', failfast=True, exit=False)

