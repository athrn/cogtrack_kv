# -*- coding: utf-8 -*-
import unittest as ut
from pprint import pprint

import setprojectpath

from testing import start_app, press
from mainapp import TheApp

from kivy.uix.label import Label


class GameController:
    def __init__(self, game_id):
        self.game_id = game_id
        self.widget_id = game_id + " widget"

class MainController(object):
    _game_ids = ['2-Back', 'Trail making', 'Morning batch']

    def get_game_ids(self):
        return MainController._game_ids
                
    def get_game_controller(self, game_id):
        return GameController(game_id)

    def save_score(self, game_id, score):
        pass


class WidgetRepository(object):
    def get_widget(self, name):
        w = Label(text='The {}'.format(name))
        w.start = lambda : None
        return w


class Tests(ut.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # NOTE: Can't use setUp since kv file is loaded once per test.
        # TODO: Figure out a safer way to write kivy tests.
        cls.app = TheApp(MainController(), WidgetRepository())
        start_app(cls.app)

    def test1_many_games(self):
        # NOTE: Use property to get only game buttons. First widget is Glue widget.
        game_buttons = self.app.game_buttons

        self.assertEqual(len(MainController._game_ids), len(game_buttons))

        for (id, btn) in zip(MainController._game_ids, game_buttons):
            self.assertEqual(id, btn.game_id)
        
    def test2_move_between_screens(self):
        game_buttons = self.app.game_buttons
        self.assert_(len(game_buttons) > 0)
        
        for game_btn in game_buttons:            
            press(game_btn)
            self.assertEqual('PlayScreen', self.app.sm.current)
            (game_widget,) = self.app.play_screen.ids.game_area.children
            self.assertEqual('The {} widget'.format(game_btn.text), game_widget.text)
            press(self.app.play_screen.ids.back_button)
            self.assertEqual('SelectScreen', self.app.sm.current)

        for game_btn in game_buttons:
            press(game_btn)
            self.assertEqual('PlayScreen', self.app.sm.current)
            press(self.app.play_screen.ids.stop_game_button)
            self.assertEqual('ScoreScreen', self.app.sm.current)
            press(self.app.score_screen.ids.score_save_button)
            self.assertEqual('SelectScreen', self.app.sm.current)

        for game_btn in game_buttons:
            press(game_btn)
            self.assertEqual('PlayScreen', self.app.sm.current)
            press(self.app.play_screen.ids.stop_game_button)
            self.assertEqual('ScoreScreen', self.app.sm.current)
            press(self.app.score_screen.ids.score_delete_button)
            self.assertEqual('SelectScreen', self.app.sm.current)

        
        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
