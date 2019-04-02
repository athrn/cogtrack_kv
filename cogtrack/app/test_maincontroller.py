# -*- coding: utf-8 -*-
import unittest as ut
import mock
from maincontroller import MainController

def make_mock_game_factory():
    mock_game_factory = mock.MagicMock()
    game, widget = mock.MagicMock(), mock.MagicMock()
    game.name = 'game name'
    widget.name = 'widget name'
    mock_game_factory.return_value = game, widget
    return mock_game_factory

def make_mock_controller(names='a b'.split()):
    c = MainController(mock.MagicMock(), make_mock_game_factory())
    for i, name in enumerate(sorted(names)):
        c.add_game(name + '_name', name + '_type', dict(x=i+1))
    
    return c.start()

class Tests(ut.TestCase):
    
    def test10_creation(self):
        gui = mock.MagicMock()
        game_factory = mock.MagicMock()
        c = MainController(gui, game_factory)
        self.assertEqual(c.gui, gui)
        self.assertEqual(c.game_factory, game_factory)
        c.gui.show_select_game.assert_not_called()
        c.start()
        c.gui.show_select_game.assert_called_once_with()
        
    def test11_add_and_list_game(self):
        c = MainController(mock.MagicMock(), mock.MagicMock())
        c.add_game('a_name', 'a_type', dict(x=1))
        c.add_game('b_name', 'b_type', dict(x=2))
        self.assertEqual(['a_name', 'b_name'], sorted(c.list_games()))

    def test12_start_game(self):
        c = make_mock_controller('a b'.split())
        self.assertEqual(['a_name', 'b_name'], sorted(c.list_games()))

        c.start_game('b_name')
        c.game_factory.assert_called_once_with('b_type', dict(x=2))
        self.assertEqual('game name', c.current_game.name)
        c.gui.show_game.assert_called_once()
        c.current_game.start.assert_called_once_with()
        self.assertEqual(c.stop_game, c.current_game.on_game_over)
        
    def test13_cancel_game(self):
        c = make_mock_controller('a b'.split())
        c.start_game('a_name')
        c.gui.show_select_game.assert_called_once_with()
        c.cancel_game()
        
        calls = [a[0] for a in c.gui.mock_calls]
        self.assertEqual('show_select_game show_game show_select_game'.split(), calls)
        self.assertIsNone(c.current_game)

    def test14_user_stop_game(self):
        c = make_mock_controller('a b'.split())
        c.start_game('a_name')
        c.gui.show_select_game.assert_called_once_with()
        c.stop_game()
        
        calls = [a[0] for a in c.gui.mock_calls]
        self.assertEqual('show_select_game show_game show_score'.split(), calls)
        self.assertIsNotNone(c.current_game)

    def test15_game_over(self):
        c = make_mock_controller('a b'.split())
        c.start_game('a_name')
        c.gui.show_select_game.assert_called_once_with()
        c.current_game.on_game_over()
        
        calls = [a[0] for a in c.gui.mock_calls]
        self.assertEqual('show_select_game show_game show_score'.split(), calls)
        self.assertIsNotNone(c.current_game)

        calls = [a[0] for a in c.current_game.mock_calls]
        self.assertEqual('start stop score'.split(), calls)

    def test16_discard_score(self):
        c = make_mock_controller('a b'.split())
        c.start_game('b_name')
        c.stop_game()
        c.discard_score()
        
        calls = [a[0] for a in c.gui.mock_calls]
        self.assertEqual('show_select_game show_game show_score show_select_game'.split(), calls)
        self.assertIsNone(c.current_game)

    def test17_save_score(self):
        # TODO:
        pass
        # c = make_mock_controller('a b'.split())
        # c.start_game('b_name')
        # c.stop_game()
        # c.save_score()
        
        # calls = [a[0] for a in c.gui.mock_calls]
        # self.assertEqual('show_select_game show_game show_score show_select_game'.split(), calls)
        # self.assertIsNone(c.current_game)


        
    def test21_stop_and_start_a_new_game(self):
        c = make_mock_controller('a b c'.split())
        c.start_game('b_name')
        c.game_factory.assert_called_once_with('b_type', dict(x=2))
        c.cancel_game()
        c.start_game('a_name')
        c.game_factory.assert_called_with('a_type', dict(x=1))
        c.stop_game()
        c.discard_score()
        c.start_game('c_name')
        c.game_factory.assert_called_with('c_type', dict(x=3))

    def test22_start_with_no_games(self):
        c = make_mock_controller(''.split())
        self.assertEqual([], c.list_games())

        
        
        
        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
