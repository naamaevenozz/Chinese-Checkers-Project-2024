import unittest
from playerNamesScreen import PlayerNamesScreen

class TestPlayerNamesScreen(unittest.TestCase):
    def test_num_players_positive_integer(self):
        with self.assertRaises(ValueError):
            PlayerNamesScreen(0)
        with self.assertRaises(ValueError):
            PlayerNamesScreen(-1)

    def test_submit_button(self):
        num_players = 2
        player_screen = PlayerNamesScreen(num_players)
        player_screen.submit_names()

    def test_submit_names_duplicate_names(self):
        num_players = 2
        player_screen = PlayerNamesScreen(num_players)
        player_screen.player_names = ["Player1", "Player1"]
        player_screen.submit_names()

    def test_submit_names_invalid_names(self):
        num_players = 1
        player_screen = PlayerNamesScreen(num_players)
        player_screen.player_names = ["Player1"]
        player_screen.submit_names()

    def test_submit_names_exception(self):
        num_players = 1
        player_screen = PlayerNamesScreen(num_players)
        player_screen.player_names = [Exception]
        player_screen.submit_names()

if __name__ == "__main__":
    unittest.main()
