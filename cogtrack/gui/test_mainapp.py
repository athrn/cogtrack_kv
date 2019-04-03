# -*- coding: utf-8 -*-
import unittest as ut
from pprint import pprint

# from kivy.tests.common import GraphicUnitTest

from testing import start_app, press
from mainapp import TheApp, format_score

from kivy.uix.label import Label

from cogtrack.app.maincontroller import MainController

import mock




def mock_game_factory(game_type, game_settings):
    widget = Label(text='The {} widget'.format(game_settings['name']))
    game = mock.MagicMock()
    game.name = game_settings['name']
    game.score.return_value = dict(x=1, y=2.0, name=game.name)
    # HACK: MainController relies on callback from game to switch screens.
    game.stop.side_effect = lambda : game.on_stop()
    game.cancel.side_effect = lambda : game.on_cancel()
    return game, widget

 

class WidgetRepository(object):
    def get_widget(self, name):
        w = Label(text='The {}'.format(name))
        w.start = lambda : None
        return w

# TODO: Split tests into MainController tests and MainApp tests.

mock_game_names = ['2-Back', 'Trail making', 'Morning batch']

def find_game_buttons(app):
    # NOTE: Return only game buttons. Ignore Space
    return [btn for btn in app.select_screen.ids.select_game_buttons.children if btn.text.strip()]


def make_mock_controller(gui):
    controller = MainController(gui, game_factory=mock_game_factory)
    for name in mock_game_names:
        controller.add_game(name, 'GameType', {'name': name})
    return controller

class Tests(ut.TestCase):
# class Tests(GraphicUnitTest):
    
    @classmethod
    def setUpClass(cls):
        # TODO: Don't know how to do this...
        # setkivyresourcepath.set_kivy_resource_path()
        # print(setkivyresourcepath.resource_paths)
        # NOTE: Can't use setUp since kv file is loaded once per test.
        # TODO: Figure out a safer way to write kivy tests.
        cls.app = TheApp()
        # NOTE: Controller init auto-sets gui.controller
        cls.controller = make_mock_controller(cls.app)
        # cls.app.controller = controller
        start_app(cls.app)

    def setUp(self):
        self.app.show_select_game()

    def test1_many_games(self):
        # NOTE: Use property to get only game buttons. First widget is Glue widget.
        game_buttons = find_game_buttons(self.app)

        self.assertEqual(3, len(game_buttons))

        for (id, btn) in zip(sorted(mock_game_names), game_buttons):
            self.assertEqual(id, btn.game_id)
        

        
        
    def test22_play_and_stop(self):
        game_buttons = find_game_buttons(self.app)
        self.assert_(len(game_buttons) > 0)

        self.assertEqual('SelectScreen', self.app.sm.current)
        
        for game_btn in game_buttons:            
            press(game_btn)
            self.assertEqual('PlayScreen', self.app.sm.current)
            (game_widget,) = self.app.play_screen.ids.game_area.children
            # HACK: Need to access the game object to check stop, start and cancel was called
            game = self.app.controller.current_game
            
            self.assertEqual('The {} widget'.format(game_btn.text), game_widget.text)
            game.start.assert_called_once_with()
            
            press(self.app.play_screen.ids.stop_game_button)            
            game.stop.assert_called_once_with()
            game.cancel.assert_not_called()
            
            self.assertEqual('ScoreScreen', self.app.sm.current)

            e = format_score(dict(name=game.name, x=1, y=2.0))
            self.assertEqual(e, self.app.score_screen.ids.score_text_area.text)



    def test23_play_and_cancel(self):
        game_buttons = find_game_buttons(self.app)
        for game_btn in game_buttons:
            press(game_btn)
            self.assertEqual('PlayScreen', self.app.sm.current)
            press(self.app.play_screen.ids.cancel_game_button)
            self.assertEqual('SelectScreen', self.app.sm.current)

    def test23_play_and_discard_score(self):
        game_buttons = find_game_buttons(self.app)
        for game_btn in game_buttons:
            press(game_btn)
            self.assertEqual('PlayScreen', self.app.sm.current)
            press(self.app.play_screen.ids.stop_game_button)
            self.assertEqual('ScoreScreen', self.app.sm.current)
            press(self.app.score_screen.ids.score_discard_button)
            self.assertEqual('SelectScreen', self.app.sm.current)


    def test20_show_score(self):
        score = dict(x=1, y=2.0, name='A Name')
        self.app.show_score(score)
        e = format_score(score)
        self.assertEqual(e, self.app.score_screen.ids.score_text_area.text)


if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
