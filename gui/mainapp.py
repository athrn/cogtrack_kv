# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.factory import Factory
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
        return root

    @property
    def game_buttons(self):
        # NOTE: Return only game buttons. Ignore Glue
        return [btn for btn in self.select_screen.ids.select_game_buttons.children if btn.text.strip()]

    def on_start(self):
        self.select_screen.ids.select_game_buttons.clear_widgets()

        # TODO: BUG: Bug workaround. text not set on first button for unknown reason
        btn = Factory.SelectGameButton(game_id='bug workaround')
        
        for id_ in reversed(self.controller.get_game_ids()):
            btn = Factory.SelectGameButton(game_id=id_)
            self.select_screen.ids.select_game_buttons.add_widget(btn)

        self.select_screen.ids.select_game_buttons.add_widget(Factory.Glue())

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

    
