from kivy.uix.label import Label
# TODO: REVIEW: run_widget vs start_app and stuff used in tests. How to unit test kivy dependent code?
from demo import run_widget

from tools import *



def run():
    label = Label(text='Wait...', font_size='128sp')

    def set_label_text(t):
        label.text = 'Done!'

    schedule(2, set_label_text)
    run_widget(label)
    



if __name__ == "__main__":
    run()


    
