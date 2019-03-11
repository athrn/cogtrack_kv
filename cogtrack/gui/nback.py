import tools
from kivy.uix.boxlayout import BoxLayout

if __name__ != "__main__":
    # Prevent double loading of kv file when executing as script
    import base    
    tools.load_kv(__file__)
    
# NOTE: Must match definition in kv file. I.e. boxlayout and not widget
# TODO: Review. There is still re-declaration of NBack
class NBack(BoxLayout):

    def __init__(self):
        BoxLayout.__init__(self)
        self.on_match = lambda : None
        self.on_no_match = lambda : None

    def show_score(self,
                  correct_match,
                  correct_no_match,
                  wrong_match,
                  wrong_no_match,
                  no_response):

        ids = self.ids.score_bar.ids
        ids.correct_match.score = correct_match
        ids.correct_no_match.score = correct_no_match
        ids.wrong_match.score = wrong_match
        ids.wrong_no_match.score = wrong_no_match
        ids.no_response.score = no_response

    def set_callbacks(self, on_match, on_no_match):
        self.on_match = on_match
        self.on_no_match = on_no_match

    def show_symbol(self, symbol):
        self.ids.show_symbol.text = symbol

    # def show_score(self, correct_match, correct_no_match, wrong_match, wrong_no_match, no_response):

    #     pass

    @classmethod
    def make(cls,
             game_factory,
             n_back=2,
             max_rounds=20,
             show_symbol_interval=1,
             next_symbol_interval=3):

        widget = cls()
        game = game_factory(show_symbol=widget.show_symbol,
                            show_score=widget.show_score,
                            schedule=tools.schedule,
                            n_back=n_back,
                            max_rounds=max_rounds,
                            show_symbol_interval=show_symbol_interval,
                            next_symbol_interval=next_symbol_interval)

        widget.on_match = game.on_match
        widget.on_no_match = game.on_no_match

        widget.game = game
        return widget


        
        




if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_nback', failfast=True, exit=False)

    from nbackdemo import run
    run()
