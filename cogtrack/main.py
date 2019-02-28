from kivy.lang import Builder
from kivy.app import App

from kivy.config import Config
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'width', 540)
Config.set('graphics', 'height', 960)

import cogtrack.game
import cogtrack.gui

def make_nback():
    gui = cogtrack.gui.nback.NBack()
    game = cogtrack.game.nback.NBack()
    return gui


class CogTrackApp(App):
    def build_config(self, config):
        config.setdefaults('dummy_section', {'x': 1,
                                             'y': 1,
                                             })

    def build(self):
        return make_nback() 
        


if __name__ == "__main__":
    app = CogTrackApp()
    app.run()
