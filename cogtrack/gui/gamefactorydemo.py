# -*- coding: utf-8 -*- 
from gamefactory import make_game
from demo import run_widget

def run():
    g = make_game('nback')
    g.start()
    run_widget(g.widget)




if __name__ == "__main__":
    run()
