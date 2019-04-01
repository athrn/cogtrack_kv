# -*- coding: utf-8 -*-

import abc

# Used to keep mock controller synced with main controller
class IMainController:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add_game(self, game_name, game_type, settings):
        pass

    @abc.abstractmethod
    def start_game(self, game_name):
        pass

    @abc.abstractmethod
    def list_games(self):
        pass

    @abc.abstractmethod
    def save_score(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def show_score(self):
        pass

    @abc.abstractmethod
    def show_select_game(self):
        pass

