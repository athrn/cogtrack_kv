import config

from kivy.lang import Builder

from demo import run_widget        

if __name__ == "__main__":
    root = Builder.load_file('./mainapp.kv')
    run_widget(root)

