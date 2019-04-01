# -*- coding: utf-8 -*-

def do_nothing():
    pass

class Game(object):
    def __init__(self):
        self.is_running = False

        # Callbacks
        self.on_start = do_nothing
        self.on_stop = do_nothing
        self.on_cancel = do_nothing

    def stop(self):
        # NOTE: Must set status before calling on_stop.
        #       callback may test self.status and call stop again.
        self.is_running = False
        self.on_stop()
        return self

    def start(self):
        self.is_running = True
        self.on_start()
        return self

    def cancel(self):
        self.is_running = False
        self.on_cancel()
        return self
