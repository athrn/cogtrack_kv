# from kivy.lang import Builder

from demo import run_widget


def run():
    import nback
    root = nback.NBack()
    run_widget(root)

# def run2():
#     # nback.kv has no main "root" widget. They all extend stuff.
#     root = Builder.load_file('nback.kv')
#     run_widget(root)
    


if __name__ == "__main__":
    run()


    
