# from kivy.lang import Builder
# from kivy.app import App

# TODO: Move to GUI? Keep all kivy related code in gui
from kivy.config import Config
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'width', 540)
Config.set('graphics', 'height', 960)

import os
from kivy.resources import resource_add_path


import cogtrack.game
from cogtrack.gui.mainapp import TheApp
from cogtrack.gui.gamefactory import game_factory
from cogtrack.app.maincontroller import MainController



def main():
    # HACK: Add gui to resource path to find sub-dir icons
    # TODO: Figure out what to do with resource paths.
    resource_add_path(os.path.join(os.path.dirname(__file__), 'gui'))
    
    gui = TheApp()
    controller = MainController(gui, game_factory)
    controller.add_game('2-Back', 'nback', dict(n_back=2))
    gui.run()



if __name__ == "__main__":
    main()
