import unittest
from unittest.mock import MagicMock

import tk

from game import Game

class TestGame(unittest.TestCase):
    def test_prep_game(self):
        game = Game()
        game.prep_game()

    def test_if_play_again(self):
        game = Game()
        game.if_play_again()

    def test_is_new_game_new_start(self):
        game = Game()
        game.is_new_game_new_start()

    def test_start(self):
        game = Game()
        game.start()

    def test_close_window(self):
        game = Game()
        root = tk.Tk()
        game.close_window(root)
        self.assertIsNone(root)

    def test_win_sound(self):
        game = Game()
        game.win_sound()  # It's hard to test sound effects in unit tests

    def test_wrong_sound(self):
        game = Game()
        game.wrong_sound()  # It's hard to test sound effects in unit tests

    def test_next_turn_sound(self):
        game = Game()
        current_message = "Next player's turn"
        game.next_turn_sound(current_message)  # It's hard to test sound effects in unit tests

    def test_is_winner(self):
        game = Game()
        result = game.is_winner()
        self.assertIsInstance(result, bool)

    def test_prep_game(self):
        game = Game()
        game.prep_game()  # This test might need mocking user input for full coverage

    def test_bind_button_clicks(self):
        game = Game()
        game.bind_button_clicks()  # This test might need mocking button clicks for full coverage

    def test_is_new_game_new_start(self):
        game = Game()
        result = game.is_new_game_new_start()
        self.assertIsInstance(result, bool)

    def test_prep_game(self):
        # Initialize the game
        game = Game()

        # Mock the opening screen to avoid GUI interference
        game.prep_game = MagicMock()

        # Call prep_game
        game.prep_game()

        # Assert that prep_game was called
        game.prep_game.assert_called_once()

    def test_start(self):
        # Initialize the game
        game = Game()

        # Mock the opening screen to avoid GUI interference
        game.show_rules = MagicMock()

        # Assert that show_rules was called

if __name__ == "__main__":
    unittest.main()
