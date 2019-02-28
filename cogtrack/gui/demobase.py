from kivy.lang import Factory
from kivy.uix.boxlayout import BoxLayout
from demo import run_widget
from tools import load_kv

# import theme

def add_widgets(layout):
    for name in 'EmptySquare Space BaseLabel BaseButton IconButton'.split():
        layout.add_widget(Factory.get(name)(text=name))
    

def run():
    load_kv("base.kv")
    root = BoxLayout(orientation='vertical')

    hlayout = BoxLayout(orientation='horizontal')
    root.add_widget(hlayout)
    add_widgets(hlayout)
    
    hlayout = BoxLayout(orientation='horizontal')
    root.add_widget(hlayout)
    hlayout.add_widget(Factory.BaseLabel(bg=(1.,0,0,1), text="Red"))
    hlayout.add_widget(Factory.BaseLabel(bg=(0,1.,0,1), text="Green"))
    
    add_widgets(root)
        
    # root.add_widget(Factory.BaseLabel(text='BaseLabel'))
    # root.text = "X"
    run_widget(root)

# def run2():
#     # nback.kv has no main "root" widget. They all extend stuff.
#     root = Builder.load_file('nback.kv')
#     run_widget(root)
    


if __name__ == "__main__":
    run()


    
