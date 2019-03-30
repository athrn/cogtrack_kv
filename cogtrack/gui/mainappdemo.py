# import setprojectpath

if __name__ == "__main__":
    from mainapp import TheApp
    from test_mainapp import MainController
    TheApp(MainController()).run()

