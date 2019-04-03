# import setprojectpath

def run():
    from mainapp import TheApp
    from test_mainapp import make_mock_controller
    app = TheApp()
    controller = make_mock_controller(app)
    app.run()


if __name__ == "__main__":
    run()
