from demo import run_widget


def run():
    import nbackwidget
    nback = nbackwidget.NBackWidget()

    nback.show_symbol("Y")
    nback.set_callbacks(on_match=lambda : nback.show_symbol("M"),
                        on_no_match=lambda : nback.show_symbol("N"),
                        )
    
    nback.show_score(1,2,3,4,5)
    
    run_widget(nback)

    


if __name__ == "__main__":
    run()


    
