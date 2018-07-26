from kivy.lang import Builder
from kivy.base import EventLoop

# NOTE: TODO: This is a non-standard and probably non-safe way to initialize the app for unit testing.
def start_app(app):    
    EventLoop.ensure_window()
    win = EventLoop.window

    # HACK: Taken from App.run. Probably unsafe in many ways.
    app._app_window = win
    app.root = app.build()
    app.window = win
    app.dispatch('on_start')

# def start_app(app):
#     from kivy.interactive import InteractiveLauncher
#     i = InteractiveLauncher(app)
#     i.run()


def press(widget):
    widget.dispatch('on_press')
