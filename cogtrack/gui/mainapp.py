# -*- coding: utf-8 -*-

# import setkivyresourcepath
# setkivyresourcepath.set_kivy_resource_path()

from kivy.app import App
from kivy.factory import Factory
from tools import load_kv

# HACK: Must load base.py before loading mainapp.kv. mainapp depends on base but can't #include for whatever reason
import base

def format_score(score):
    return '\n'.join('{}: {}'.format(k,v) for k,v in sorted(score.items()))
        

# NOTE: Must NOT name the app the same as the kv file. The auto-import happens BEFORE build is called.
class TheApp(App):

    def __init__(self):
        App.__init__(self)
        self.controller = None

    def build(self):
        root = load_kv(__file__)        
        self.sm = root
        self.select_screen = root.ids.select_screen
        self.play_screen = root.ids.play_screen
        self.score_screen = root.ids.score_screen
        return root


    def on_start(self):
        self.select_screen.ids.select_game_buttons.clear_widgets()

        # TODO: BUG: Bug workaround. text not set on first button for unknown reason
        dummy_workaround = Factory.SelectGameButton(game_id='bug workaround')
        
        for id_ in reversed(self.controller.list_games()):
            btn = Factory.SelectGameButton(game_id=id_)
            self.select_screen.ids.select_game_buttons.add_widget(btn)

        self.select_screen.ids.select_game_buttons.add_widget(Factory.Space())

    def show_game(self, widget):
        game_area = self.play_screen.ids.game_area
        game_area.clear_widgets()
        game_area.add_widget(widget)
        
        self.sm.current = self.play_screen.name
        # game.start()

    def show_select_game(self):
        self.sm.current = self.select_screen.name


    def show_score(self, score):
        self.score_screen.ids.score_text_area.text = format_score(score)
        self.sm.current = self.score_screen.name


if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_mainapp', failfast=True, exit=False)

    from mainappdemo import run
    run()

    
