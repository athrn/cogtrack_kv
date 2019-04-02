1# -*- coding: utf-8 -*-
import unittest as ut
import time

from nbackgame import NBackGame, fixed_chars, MATCH, NO_MATCH, NO_RESPONSE
from mock import MagicMock, call

def score_sanity_check(nback, offset=0):
    # TODO: Sanity check. Doesn't work for no response.
    responses = 0
    score = nback.score()
    for r in score:
        for m in score[r]:
            responses += score[r][m]

    assert nback.current_round - offset == responses

def assert_equal(x, y):
    if(x != y):
        raise AssertionError('{} != {}'.format(x,y))

def assert_score(nback,
                 correct_match=0,
                 wrong_match=0,
                 correct_no_match=0, 
                 wrong_no_match=0,
                 no_response_match=0,
                 no_response_no_match=0):
    score = nback.score()
    assert_equal(correct_match, score[MATCH][True])
    assert_equal(correct_no_match, score[NO_MATCH][False])
    assert_equal(wrong_match, score[MATCH][False])
    assert_equal(wrong_no_match, score[NO_MATCH][True])
    assert_equal(no_response_match, score[NO_RESPONSE][True])
    assert_equal(no_response_no_match, score[NO_RESPONSE][False])

    
 
def call_string(m):
    " Concatenate all calls and return as string call('A'), call('B') -> AB" 
    return ''.join([c[0][0] for c in m.call_args_list])

class Tests(ut.TestCase):

    def test10_warmup(self):
        nback = NBackGame(n_back = 2)
        nback.start()
        
        self.assertFalse(nback.is_after_warmup())
        nback.next_char()
        self.assertFalse(nback.is_after_warmup())
        nback.next_char()
        self.assertFalse(nback.is_after_warmup())
        nback.next_char()
        self.assertTrue(nback.is_after_warmup())
        nback.next_char()
        self.assertTrue(nback.is_after_warmup())

    def test11_current_round(self):
        nback = NBackGame(n_back = 2).start()

        self.assertEqual(-2, nback.current_round)
        nback.next_char()
        self.assertEqual(-1, nback.current_round)
        nback.next_char()
        self.assertEqual(0, nback.current_round)
        nback.next_char()
        self.assertEqual(1, nback.current_round)
        nback.next_char()
        self.assertEqual(2, nback.current_round)


    def test12_max_rounds(self):        
        nback = NBackGame(max_rounds = 1,
                          n_back = 1).start()

        self.assertFalse(not nback.is_running)
        nback.next_char()
        nback.next_char() # Round 1
        self.assertFalse(not nback.is_running)
        nback.next_char() # Stop
        self.assertTrue(not nback.is_running)

        nback = NBackGame(max_rounds = 2,
                      n_back = 1).start()

        self.assertFalse(not nback.is_running)
        nback.next_char()
        nback.next_char() # Round 1
        self.assertFalse(not nback.is_running)
        nback.next_char() # Round 2
        self.assertFalse(not nback.is_running)
        nback.next_char() # Stop
        self.assertTrue(not nback.is_running)

        nback = NBackGame(max_rounds = 2,
                          n_back = 2).start()

        self.assertFalse(not nback.is_running)
        nback.next_char()
        nback.next_char()
        nback.next_char() # Round 1
        self.assertFalse(not nback.is_running)
        nback.next_char() # Round 2
        self.assertFalse(not nback.is_running)
        nback.next_char() # Stop
        self.assertTrue(not nback.is_running)

    def test2_next_char(self):
        show_symbol=MagicMock()
        nback = NBackGame(show_symbol=show_symbol,
                          char_generator=fixed_chars("ACB")).start()
        
        nback.next_char()
        show_symbol.assert_called_once_with('A')
        nback.next_char()
        show_symbol.assert_called_with('C')
        nback.next_char()
        show_symbol.assert_called_with('B')
        
    
    def test3_is_current_symbol_a_match(self):
        show_symbol=MagicMock()
        nback = NBackGame(max_rounds = 8,
                      n_back=2,
                      show_symbol=show_symbol,
                      char_generator = fixed_chars("XAXBXCDXEX")).start()
        
        nback.next_char()
        self.assertFalse(nback.is_current_symbol_a_match())

        nback.next_char()
        self.assertFalse(nback.is_current_symbol_a_match())

        nback.next_char()
        self.assertEqual('XAX', call_string(show_symbol))
        self.assertTrue(nback.is_current_symbol_a_match())

        nback.next_char()
        self.assertFalse(nback.is_current_symbol_a_match())

        nback.next_char()
        self.assertEqual('XAXBX', call_string(show_symbol))
        self.assertTrue(nback.is_current_symbol_a_match())

        nback.next_char()
        self.assertFalse(nback.is_current_symbol_a_match())

        nback.next_char()
        self.assertFalse(nback.is_current_symbol_a_match())

        nback.next_char()
        self.assertFalse(nback.is_current_symbol_a_match())

        nback.next_char()
        self.assertEqual('XAXBXCDXE', call_string(show_symbol))
        self.assertFalse(nback.is_current_symbol_a_match())

        nback.next_char()
        self.assertTrue(nback.is_current_symbol_a_match())

    
    def test4_history(self):
        nback = NBackGame(n_back=2,
                          char_generator=fixed_chars("ABCDE")).start()

        self.assertEqual(['', '', ''], nback.history)
        nback.next_char()
        self.assertEqual(['A', '', ''], nback.history)
        nback.next_char()
        self.assertEqual(['A', 'B', ''], nback.history)
        nback.next_char()
        self.assertEqual(['A', 'B', 'C'], nback.history)
        nback.next_char()
        self.assertEqual(['D', 'B', 'C'], nback.history)
        nback.next_char()
        self.assertEqual(['D', 'E', 'C'], nback.history)

    def test51_user_correct_interaction(self):
        nback = NBackGame(n_back=2,
                      char_generator=fixed_chars("AXCXE")).start()

        nback.next_char()
        nback.next_char()
        nback.next_char()
        nback.user_no_match()
        assert_score(nback, 0, 0, 1, 0)
        
        nback.next_char()
        nback.user_match()
        assert_score(nback, 1, 0, 1, 0)
        
        nback.next_char()
        nback.user_no_match()
        assert_score(nback, 1, 0, 2, 0)

    def test52_user_wrong_interaction(self):
        nback = NBackGame(n_back=2,
                      char_generator=fixed_chars("AXCXE")).start()

        nback.next_char()
        nback.next_char()
        nback.next_char()
        nback.user_match()
        assert_score(nback, 0, 1, 0, 0)
        
        nback.next_char()
        nback.user_no_match()
        assert_score(nback, 0, 1, 0, 1)
        
        nback.next_char()
        nback.user_match()
        assert_score(nback, 0, 2, 0, 1)
        
        score_sanity_check(nback)

    def test53_user_no_response(self):
        nback = NBackGame(n_back=2,
                          char_generator=fixed_chars("AXCXE")).start()

        nback.next_char()
        nback.next_char()
        nback.next_char()
        nback.next_char()
        assert_score(nback, 0, 0, 0, 0, 0, 1) # NOTE: Delayed scoring for no_response
        nback.next_char()
        assert_score(nback, 0, 0, 0, 0, 1, 1)
        nback.next_char()
        assert_score(nback, 0, 0, 0, 0, 1, 2)
                
        score_sanity_check(nback, 1)

    def test54_user_interaction_during_warmup_is_ignored(self):
        nback = NBackGame(n_back=2,
                      char_generator=fixed_chars("AXCXE")).start()

        nback.next_char()
        nback.user_match()
        assert_score(nback, 0, 0, 0, 0)
        
        nback.next_char()
        nback.user_no_match()
        assert_score(nback, 0, 0, 0, 0)
        score_sanity_check(nback)


    def test61_reaction_time(self):
        nback = NBackGame(n_back=2,
                          char_generator=fixed_chars("X")).start()

        nback.next_char()
        nback.next_char()
        nback.next_char()

        time.sleep(0.1)
        nback.user_match()
        t = nback.reaction_time[MATCH][True].sum
        self.assert_(0.1 <= t and t <= 0.2)

        nback.next_char()
        time.sleep(0.2)
        nback.user_match()
        t = nback.reaction_time[MATCH][True].sum
        self.assert_(0.3 <= t and t <= 0.31)
        t = nback.reaction_time[MATCH][True].avg
        self.assert_(0.15 <= t and t <= 0.16)

    def test71_user_stop_before_response(self):
        nback = NBackGame(n_back=2, char_generator=fixed_chars('X')).start()

        # Warmup
        nback.next_char()
        nback.next_char()
        # Rounds
        nback.next_char()
        nback.user_match()
        nback.next_char()
        nback.stop()
        assert_score(nback, 1, 0, 0, 0)
        # NOTE: current_round > sum of responses
        self.assertEqual(2, nback.current_round)

        # Continued action does nothing
        nback.user_match()
        assert_score(nback, 1, 0, 0, 0)

        nback.next_char()
        self.assertEqual(2, nback.current_round)
        nback.user_match()
        assert_score(nback, 1, 0, 0, 0)
        
    def test72_user_stop_after_response(self):
        nback = NBackGame(n_back=1, char_generator=fixed_chars('X')).start()
        # Warmup
        nback.next_char()
        # Rounds
        nback.next_char()
        nback.user_match()
        nback.stop()
        assert_score(nback, 1, 0, 0, 0)

    def test72_user_stop_after_warmup(self):
        nback = NBackGame(n_back=1, char_generator=fixed_chars('X')).start()
        # Warmup
        nback.next_char()
        nback.stop()
        assert_score(nback, 0, 0, 0, 0)

    def test72_user_stop_during_warmup(self):
        nback = NBackGame(n_back=2, char_generator=fixed_chars('X')).start()
        nback.next_char()
        nback.stop()
        assert_score(nback, 0, 0, 0, 0)

    def test72_user_stop_(self):
        nback = NBackGame(n_back=1, char_generator=fixed_chars('X')).start()
        nback.next_char()
        nback.next_char() # Round 1 
        nback.next_char() # No Response
        nback.stop()
        assert_score(nback, 0, 0, 0, 0, 1, 0)

    def test8_nback(self):
        nback = NBackGame(n_back = 1,
                          char_generator = fixed_chars("CCCCDE")).start()
        nback.next_char() # Warmup
        nback.next_char()
        nback.user_match()
        nback.next_char()
        nback.user_match()
        nback.next_char()
        nback.user_match()
        nback.next_char()
        nback.user_no_match()
        nback.next_char()
        nback.user_no_match()
        assert_score(nback, 3,0,2,0)

        nback = NBackGame(n_back = 2,
                          char_generator = fixed_chars("CCCCDE")).start()
        nback.next_char() # Warmup
        nback.next_char() # Warmup
        nback.next_char()
        nback.user_match()
        nback.next_char()
        nback.user_match()
        nback.next_char()
        nback.user_no_match()
        nback.next_char()
        nback.user_no_match()
        assert_score(nback, 2,0,2,0)
    
        nback = NBackGame(n_back = 3,
                          char_generator = fixed_chars("CCCCDE")).start()
        nback.next_char() # Warmup
        nback.next_char() # Warmup
        nback.next_char() # Warmup
        nback.next_char()
        nback.user_match()
        nback.next_char()
        nback.user_no_match()
        nback.next_char()
        nback.user_no_match()
        assert_score(nback, 1,0,2,0)

    def test9_double_user_response(self):
        nback = NBackGame(n_back=1, char_generator=fixed_chars('X')).start()
        nback.next_char() # Warmup
        nback.next_char()
        nback.user_match()
        nback.user_match()
        nback.user_no_match()
        assert_score(nback, correct_match=1)

    def testA_callbacks(self):
        schedule=MagicMock()
        show_symbol=MagicMock()
        show_score=MagicMock()
        
        nback = NBackGame(n_back=1,
                      char_generator=fixed_chars('AABBCD'),
                      show_symbol=show_symbol,
                      show_score=show_score,
                      schedule=schedule).start()
        hide_call = call(nback.show_symbol_interval, nback.hide_symbol)
        next_call = call(nback.next_symbol_interval, nback.next_char)

        show_symbol.assert_not_called()
        nback.next_char()
        show_symbol.assert_called_once_with('A')
        schedule.assert_has_calls([hide_call, next_call])
        
        nback.next_char()
        show_symbol.assert_called_with('A')
        schedule.assert_has_calls([hide_call, next_call]*2)
        nback.user_match()
        show_score.assert_called_once_with(correct_match=1,
                                           correct_no_match=0,
                                           wrong_match=0,
                                           wrong_no_match=0,
                                           no_response=0)

        nback.next_char()
        show_symbol.assert_called_with('B')
        schedule.assert_has_calls([hide_call, next_call]*3)
        nback.user_no_match()
        show_score.assert_called_with(correct_match=1,
                                      correct_no_match=1,
                                      wrong_match=0,
                                      wrong_no_match=0,
                                      no_response=0)

        # Display no response as "wrong"
        nback.next_char()
        show_symbol.assert_called_with('B')
        nback.next_char()
        show_symbol.assert_called_with('C')
        show_score.assert_called_with(correct_match=1,
                                      correct_no_match=1,
                                      wrong_match=0,
                                      wrong_no_match=0,
                                      no_response=1)

        nback.next_char()
        show_symbol.assert_called_with('D')
        show_score.assert_called_with(correct_match=1,
                                      correct_no_match=1,
                                      wrong_match=0,
                                      wrong_no_match=0,
                                      no_response=2)
        nback.user_match()
        show_score.assert_called_with(correct_match=1,
                                      correct_no_match=1,
                                      wrong_match=1,
                                      wrong_no_match=0,
                                      no_response=2)



    def test93_on_stop(self):
        on_game_over=MagicMock()
        nback = NBackGame(max_rounds=3, n_back=2).start()
        nback.on_game_over = on_game_over
        nback.next_char()
        nback.next_char()
        nback.next_char() # 1
        nback.next_char() # 2
        nback.next_char() # 3
        on_game_over.assert_not_called()
        nback.next_char() # Finished
        on_game_over.assert_called_once_with()
        nback.next_char() # Game over only called once
        on_game_over.assert_called_once_with()
        
        



if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
