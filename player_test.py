import unittest
from player import Player  # Import the Player class from your module

class TestPlayer(unittest.TestCase):
    def setUp(self):
        # Initialize objects that will be used in multiple tests
        self.player = Player("red", [(0, 0), (1, 1)], "Alice")

    def test_initialization(self):
        self.assertEqual(self.player.get_color(), "red")
        self.assertEqual(self.player.get_name(), "Alice")
        self.assertEqual(self.player.get_wins(), 0)
        self.assertEqual(self.player.get_losses(), 0)

    def test_update_stats(self):
        self.player.update_stats("win")
        self.assertEqual(self.player.get_wins(), 1)

        self.player.update_stats("loss")
        self.assertEqual(self.player.get_losses(), 1)

    def test_move_coord(self):
        initial_locations = self.player.get_player_current_locations()
        self.player.move_coord((0, 0), (2, 2))
        new_locations = self.player.get_player_current_locations()
        self.assertIn((2, 2), new_locations)

    def test_reset_current_locations(self):
        self.player.move_coord((0, 0), (2, 2))
        self.player.reset_current_locations()
        self.assertEqual(self.player.get_player_current_locations(), [(0, 0), (1, 1)])

if __name__ == '__main__':
    unittest.main()
