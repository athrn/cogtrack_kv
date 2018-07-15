from kivy.lang import Builder
from kivy.app import App
import akivy

from kivy.config import Config
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'width', 500)
Config.set('graphics', 'height', 800)



class CogTrackApp(App):
    def build_config(self, config):
        config.setdefaults('dummy_section', {'x': 1,
                                             'y': 1,
                                             })

    def build(self):
        return Builder.load_file('./gui/main.kv')        
        


if __name__ == "__main__":
    app = CogTrackApp()
    app.run()
