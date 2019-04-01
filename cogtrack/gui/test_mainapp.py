# -*- coding: utf-8 -*-
import unittest as ut
from pprint import pprint

# from kivy.tests.common import GraphicUnitTest

from testing import start_app, press
from mainapp import TheApp

from kivy.uix.label import Label

from cogtrack.game.igame import IGame
from cogtrack.app.imaincontroller import IMainController

import mock

# class MockGame(IGame):
#     def __init__(self, game_id):
#         self.game_id = game_id

#     def start(self):
#         pass

#     def stop(self):
#         pass

#     def cancel(self):
#         pass
    

class MainController(IMainController):
    _game_ids = ['2-Back', 'Trail making', 'Morning batch']

    def list_games(self):
        return MainController._game_ids
                
    def start_game(self, game_id):
        widget = Label(text='The {} widget'.format(game_id))
        # game = MockGame(game_id)
        game = mock.MagicMock()
        return game, widget

    def add_game(self):
        pass

    def save_score(self):
        pass

 

class WidgetRepository(object):
    def get_widget(self, name):
        w = Label(text='The {}'.format(name))
        w.start = lambda : None
        return w


class Tests(ut.TestCase):
# class Tests(GraphicUnitTest):
    
    @classmethod
    def setUpClass(cls):
        # TODO: Don't know how to do this...
        # setkivyresourcepath.set_kivy_resource_path()
        # print(setkivyresourcepath.resource_paths)
        # NOTE: Can't use setUp since kv file is loaded once per test.
        # TODO: Figure out a safer way to write kivy tests.
        cls.app = TheApp(MainController())
        start_app(cls.app)

    def test1_many_games(self):
        # NOTE: Use property to get only game buttons. First widget is Glue widget.
        game_buttons = self.app.game_buttons

        self.assertEqual(len(MainController._game_ids), len(game_buttons))

        for (id, btn) in zip(MainController._game_ids, game_buttons):
            self.assertEqual(id, btn.game_id)
        
    def test2_play_and_stop(self):
        game_buttons = self.app.game_buttons
        self.assert_(len(game_buttons) > 0)
        
        for game_btn in game_buttons:            
            press(game_btn)
            self.assertEqual('PlayScreen', self.app.sm.current)
            (game_widget,) = self.app.play_screen.ids.game_area.children
            # HACK: Need to access the game object to check stop, start and cancel was called
            game = game_widget.game
            
            self.assertEqual('The {} widget'.format(game_btn.text), game_widget.text)
            game.start.assert_called_once_with()
            
            press(self.app.play_screen.ids.stop_game_button)            
            # game.stop.assert_called_once_with()
            # game.cancel.assert_not_called()
            
            self.assertEqual('ScoreScreen', self.app.sm.current)


    def test2_move_between_screens(self):
        game_buttons = self.app.game_buttons
        self.assert_(len(game_buttons) > 0)
        
        for game_btn in game_buttons:            
            press(game_btn)
            self.assertEqual('PlayScreen', self.app.sm.current)
            (game_widget,) = self.app.play_screen.ids.game_area.children
            self.assertEqual('The {} widget'.format(game_btn.text), game_widget.text)
            press(self.app.play_screen.ids.cancel_game_button)
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
    
