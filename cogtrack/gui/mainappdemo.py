# import setprojectpath

if __name__ == "__main__":
    from mainapp import TheApp
    from test_mainapp import make_mock_controller
    app = TheApp()
    controller = make_mock_controller(app)
    app.controller = controller
    app.run()

