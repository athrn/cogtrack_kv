from demo import run_widget


def run():
    import nback
    nback = nback.NBack()

    nback.show_symbol("Y")
    nback.set_callbacks(on_match=lambda : nback.show_symbol("M"),
                        on_no_match=lambda : nback.show_symbol("D"),
                        )

    nback.show_score(1,2,3,4,5)
    
    run_widget(nback)

    


if __name__ == "__main__":
    run()


    
