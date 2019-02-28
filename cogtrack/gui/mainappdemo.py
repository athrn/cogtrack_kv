import setprojectpath

if __name__ == "__main__":
    from mainapp import TheApp
    from test_mainapp import WidgetRepository, MainController
    TheApp(MainController(), WidgetRepository()).run()

