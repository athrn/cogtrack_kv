# -*- coding: utf-8 -*-

from kivy.app import App
from tools import load_kv

# NOTE: Must NOT name the app the same as the kv file. The auto-import happens BEFORE build is called.
class TheApp(App):

    def __init__(self, main_controller, widget_repository):
        App.__init__(self)
        self.controller = main_controller
        self.widget_repository = widget_repository
    
    def build(self):
        root = load_kv(__file__)        
        self.sm = root
        self.select_screen = root.ids.select_screen
        self.play_screen = root.ids.play_screen
        self.score_screen = root.ids.score_screen
        # self.select_game_buttons = self.select_screen.ids.select_game_buttons
        return root

    def start_game(self, game_id):
        game_controller = self.controller.get_game_controller(game_id)
        widget = self.widget_repository.get_widget(game_controller.widget_id)

        game_area = self.play_screen.ids.game_area
        game_area.clear_widgets()
        game_area.add_widget(widget)
        
        self.sm.current = self.play_screen.name
        widget.start()
        
        
        
        



if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_mainapp', failfast=True, exit=False)

    
