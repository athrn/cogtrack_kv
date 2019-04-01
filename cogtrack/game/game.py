# -*- coding: utf-8 -*-

def do_nothing():
    pass

class Game(object):
    def __init__(self):
        # TODO: is_running no longer needs to be in base class. 
        self.is_running = False

        # TODO: CLEANUP: Not used. Remove?
        # Callbacks
        # self.on_start = do_nothing
        # self.on_stop = do_nothing
        # self.on_cancel = do_nothing
        
        # Game Over should be used when the game ends by itself, not when forced by user interaction.
        self.on_game_over = do_nothing

    def stop(self):
        # NOTE: Must set status before calling on_stop.
        #       callback may test self.status and call stop again.
        self.is_running = False
        # self.on_stop()
        return self

    def start(self):
        self.is_running = True
        # self.on_start()
        return self

    def cancel(self):
        self.is_running = False
        # self.on_cancel()
        return self
