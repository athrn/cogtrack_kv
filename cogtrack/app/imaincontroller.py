# -*- coding: utf-8 -*-

import abc

class IMainController:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add_game(self, game_name, game_type, settings):
        raise NotImplementedError()

    @abc.abstractmethod
    def start_game(self, game_name):
        raise NotImplementedError()

    @abc.abstractmethod
    def list_games(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def save_session(self, game_name, session):
        raise NotImplementedError()
   
