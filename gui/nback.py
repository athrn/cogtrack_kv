from tools import load_kv
from kivy.uix.boxlayout import BoxLayout


if __name__ != "__main__":
    # Prevent double loading of kv file when running as script.
    load_kv(__file__)


# NOTE: Must match definition in kv file. I.e. boxlayout and not widget
class NBack(BoxLayout):

    def __init__(self):
        BoxLayout.__init__(self)
        self.on_match = lambda self_: None
        self.on_different = lambda self_: None

    # def set_score(self, correct, 

    def set_callbacks(self, on_match, on_different):
        self.on_match = on_match
        self.on_different = on_different

    def show_symbol(self, symbol):
        self.ids.show_symbol.text = symbol

if __name__ == "__main__":
    from demonback import run
    run()
