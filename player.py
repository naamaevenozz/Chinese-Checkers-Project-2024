from typing import Tuple, List

Coordinates = Tuple[int, int]

import copy


class Player:
    """
    Represents a player in the Chinese Checkers game.
    """

    def __init__(self, color: str, locations: List[Coordinates], name: str) -> None:
        """
        Initializes a Player object.

        Args:
            color (str): The color representing the player.
            locations (List[Coordinates]): List of tuples representing all the locations where the player exists.
            name (str): The name of the player.
        """
        self.__color = color
        self.__home_locations = locations
        self.__current_locations = copy.deepcopy(locations)
        self.__name = name
        self.__wins = 0
        self.__losses = 0

    def update_stats(self, result: str) -> None:
        """
        Update player's statistics based on game result.

        Args:
            result (str): Result of the game ('win' or 'loss').
        """
        if result == 'win':
            self.__wins += 1
        elif result == 'loss':
            self.__losses += 1

    def move_coord(self, current_coord: Coordinates, new_coord: Coordinates) -> None:
        """
        Update the player's current locations after a move.

        Args:
            current_coord (Coordinates): Current coordinate that the player wants to move from.
            new_coord (Coordinates): Target coordinate where the player wants to move.
        """
        self.__current_locations.remove(current_coord)
        self.__current_locations.append(new_coord)

    def get_player_home_locations(self) -> List[Coordinates]:
        """
        Get a list of all the home locations of the player.

        Returns:
            List[Coordinates]: A list of coordinates representing the home locations of the player.
        """
        return self.__home_locations

    def get_player_current_locations(self) -> List[Coordinates]:
        """
        Get a list of all the current locations of the player.

        Returns:
            List[Coordinates]: A list of coordinates representing the current locations of the player.
        """
        return self.__current_locations

    def reset_current_locations(self) -> None:
        """
        Reset the current locations of the player to their home locations.
        """
        self.__current_locations = copy.deepcopy(self.__home_locations)

    def get_color(self) -> str:
        """
        Get the color of the player.

        Returns:
            str: The color of the player.
        """
        return self.__color

    def get_wins(self) -> int:
        """
        Get the number of wins of the player.

        Returns:
            int: The number of wins of the player.
        """
        return self.__wins

    def get_losses(self) -> int:
        """
        Get the number of losses of the player.

        Returns:
            int: The number of losses of the player.
        """
        return self.__losses

    def get_name(self) -> str:
        """
        Get the name of the player.

        Returns:
            str: The name of the player.
        """
        return self.__name
