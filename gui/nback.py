from tools import load_kv
from kivy.uix.boxlayout import BoxLayout
# from base import BaseLabel

if __name__ != "__main__":
    # Prevent double loading of kv file when running as script.
    load_kv(__file__)


# NOTE: Must match definition in kv file. I.e. boxlayout and not widget
class NBack(BoxLayout):
    pass

# class ScoreBox(BaseLabel):
#     def __init__(self):
#         self.score = 10

if __name__ == "__main__":
    from demonback import run
    run()
