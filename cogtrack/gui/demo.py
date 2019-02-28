# -*- coding: utf-8 -*-
from kivy.app import App

class TheApp(App):
    def __init__(self, root):
        App.__init__(self)
        self._build_root = root
        
    def build(self):
        return self._build_root

def run_widget(root):
    app = TheApp(root=root)
    app.run()
    return app


     


