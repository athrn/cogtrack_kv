# -*- coding: utf-8 -*-
import unittest as ut
from pprint import pprint

from testing import start_app, press
from mainapp import TheApp

from kivy.uix.label import Label


class GameController:
    def __init__(self, game_id):
        self.game_id = game_id
        self.widget_id = game_id + " widget"

class MainController(object):

    def get_game_ids():
        return ['2-Back', 'Trail making', 'Morning batch']
                
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
    def setUp(self):
        self.app = TheApp(MainController(), WidgetRepository())
        start_app(self.app)
        
    def test1_move_between_screens(self):
        game_buttons = self.app.select_screen.ids.select_game_buttons.children
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
    
