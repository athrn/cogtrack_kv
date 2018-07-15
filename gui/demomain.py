import config

from kivy.lang import Builder
from kivy.app import App
import akivy


class Dummy(App):
    def build(self):
        return Builder.load_file('./main.kv')        
        

if __name__ == "__main__":
    app = Dummy()
    app.run()
