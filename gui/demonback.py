# from kivy.lang import Builder

from demo import run_widget


def run():
    import nback
    nback = nback.NBack()

    nback.show_symbol("Y")
    nback.set_callbacks(on_match=lambda : nback.show_symbol("M"),
                        on_different=lambda : nback.show_symbol("D"),
                        )
    
    run_widget(nback)

# def run2():
#     # nback.kv has no main "root" widget. They all extend stuff.
#     root = Builder.load_file('nback.kv')
#     run_widget(root)
    


if __name__ == "__main__":
    run()


    
