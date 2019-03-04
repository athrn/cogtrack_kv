from demo import run_widget


def run():
    import nback
    nback = nback.NBack()

    nback.show_symbol("Y")
    nback.set_callbacks(on_match=lambda : nback.show_symbol("M"),
                        on_no_match=lambda : nback.show_symbol("D"),
                        )

    nback.set_score(1,2,3,4)
    
    run_widget(nback)

# def run2():
#     # nback.kv has no main "root" widget. They all extend stuff.
#     root = Builder.load_file('nback.kv')
#     run_widget(root)
    


if __name__ == "__main__":
    run()


    
