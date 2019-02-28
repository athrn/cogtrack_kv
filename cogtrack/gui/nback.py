from tools import load_kv
from kivy.uix.boxlayout import BoxLayout


if __name__ != "__main__":
    # Prevent double loading of kv file when running as script.
    load_kv(__file__)


# NOTE: Must match definition in kv file. I.e. boxlayout and not widget
class NBack(BoxLayout):

    def __init__(self):
        BoxLayout.__init__(self)
        self.on_match = lambda : None
        self.on_no_match = lambda : None

    def set_score(self,
                  correct_match,
                  correct_no_match,
                  wrong_match,
                  wrong_no_match):

        ids = self.ids.score_bar.ids
        ids.correct_match.score = correct_match
        ids.correct_no_match.score = correct_no_match
        ids.wrong_match.score = wrong_match
        ids.wrong_no_match.score = wrong_no_match

    def set_callbacks(self, on_match, on_no_match):
        self.on_match = on_match
        self.on_no_match = on_no_match

    def show_symbol(self, symbol):
        self.ids.show_symbol.text = symbol



if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_nback', failfast=True, exit=False)

    from demonback import run
    run()
