# -*- coding: utf-8 -*-

import random
from math import sqrt
import time
import itertools

import game

from cogtrack.tools.stats import Stats

# TODO: How to handle charGenerator properties? Seed?
# TODO: Probably want charGenerator with predetermined number of matches. 5/20 or so. Exakt same number of matches, just different chars and order.

NO_MATCH = 'no_match'
MATCH = 'match'
NO_RESPONSE = 'no_response'

# TODO: Create character generator with a deterministic number of matches.
# NOTE: The probability of matches must equal the probability of non matches to prevent intuitive matching.

def random_chars(chars="ABCDEF", rnd=random.randint):
    def next():
        return chars[rnd(0, len(chars)-1)]
    return next


def fixed_chars(chars="ABCDEF"):
    return itertools.cycle(chars).next


current_time = time.time


class NBackGame(game.Game):

    def __init__(self,
                 show_symbol=lambda symbol: None,
                 show_score=lambda correct_match, correct_no_match, wrong_match, wrong_no_match, no_response: None,
                 schedule=lambda time, function: None,
                 n_back=2,
                 max_rounds=10,
                 show_symbol_interval=2,
                 next_symbol_interval=3,
                 char_generator = random_chars()):

        game.Game.__init__(self)

        self.show_symbol_interval = show_symbol_interval
        self.next_symbol_interval = next_symbol_interval

        self.show_symbol = show_symbol
        self.show_score = show_score
        self.schedule = schedule
        
        self.n_back = n_back
        self.max_rounds = max_rounds
        self.char_generator = char_generator

        # TODO: Rename. Better name for the displayed symbol. Symbol? Memorized symbol?
        self.char_count = 0

        self.has_guessed = True

        self.history = ['']*(self.n_back + 1)

        self.reaction_start_time = None

        self._reset_score_and_reaction_time()

    def _reset_score_and_reaction_time(self):
        self.score = {}
        self.reaction_time = {}
        for response in [MATCH, NO_MATCH, NO_RESPONSE]:
            self.score[response] = {}
            self.reaction_time[response] = {}
            for is_match in [True, False]:
                self.score[response][is_match] = 0
                self.reaction_time[response][is_match] = Stats()


    @property
    def current_round(self):
        return self.char_count - self.n_back


    def is_after_warmup(self):
        return self.char_count > self.n_back
    
    def log_response(self, name):
        # Log response, is match, reaction time
        reaction_time = current_time() - self.reaction_start_time

        is_match = self.is_current_symbol_a_match()
        self.score[name][is_match] += 1
        self.reaction_time[name][is_match] += reaction_time

        self.show_score(correct_match=self.score[MATCH][True],
                        correct_no_match=self.score[NO_MATCH][False],
                        wrong_match=self.score[MATCH][False],
                        wrong_no_match=self.score[NO_MATCH][True],
                        no_response=self.score[NO_RESPONSE][False] + self.score[NO_RESPONSE][True],
                        )
        

    def hide_symbol(self):
        self.show_symbol('')

 
    def next_char(self):
        if not self.is_running:
            return

        if (not self.has_guessed and self.is_after_warmup()):
            self.log_response(NO_RESPONSE)

        previous_round_was_last = self.current_round == self.max_rounds
        if previous_round_was_last:
            self.stop()
            self.on_game_over()
            return

        char = self.char_generator()
        self.history[self.char_count % len(self.history)] = char
        self.char_count += 1

        self.has_guessed = False

        self.show_symbol(char)
        self.reaction_start_time = current_time()
        self.schedule(self.show_symbol_interval, self.hide_symbol)
        self.schedule(self.next_symbol_interval, self.next_char)


    def is_current_symbol_a_match(self):
        if not self.is_after_warmup():
            return False

        cur = (self.char_count - 1) % len(self.history)
        prev = (cur + 1) % len(self.history)
        return self.history[cur] == self.history[prev]

    def parse_response(self, name):
        if not self.is_running or not self.is_after_warmup():
            return

        if not self.has_guessed:
            self.log_response(name)

        self.has_guessed = True

    def user_match(self):
        self.parse_response(MATCH)

    def user_no_match(self):
        self.parse_response(NO_MATCH)
        
    def start(self):
        # TODO: Test this.
        self.schedule(0, lambda : self.show_symbol('3'))
        self.schedule(1, lambda : self.show_symbol('2'))
        self.schedule(2, lambda : self.show_symbol('1'))
        self.schedule(3, self.next_char)
        # TODO: Replace with super()
        super(type(self), self).start()
        return self


if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_nbackgame', failfast=True, exit=False)

    
