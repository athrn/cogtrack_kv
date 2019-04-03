# import setprojectpath
from mainapp import TheApp
from test_mainapp import make_mock_controller
from kivy.clock import Clock

def run():
    app = TheApp()
    controller = make_mock_controller(app)
    app.run()

def run_show_score():
    app = TheApp()
    controller = make_mock_controller(app)
    score={}
    for i, key in enumerate('abcdefghijklmnopqrstuvxyz ABCDEFGHIJKLMNOPQRSTUVXYZ'):
        score[key] = i
    Clock.schedule_once(lambda dt : app.show_score(score), 0)
    app.run()


if __name__ == "__main__":
    run_show_score()
