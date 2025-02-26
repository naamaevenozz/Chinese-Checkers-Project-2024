"""
Final project in the subject of Chinese Checkers.
Submitted by Naama Even Oz , 213710676.

Date: [31.3.2024]

Libraries required:
- tkinter (for GUI)
- tkinter.ttk (for themed widgets)
- tkinter.messagebox (for message boxes)
- tkinter.toplevel (for creating additional windows)
- pyttsx3 (for text-to-speech functionality)
- winsound (for playing sound effects)
- random (for generating random moves)
- math (for mathematical calculations)
- collections.defaultdict (for creating a default dictionary)
-copy (for deep copying lists): Python's built-in library used for creating deep copies of objects.
-unittest: This is the standard library for writing and running tests in Python. It comes bundled with Python, so there's no need to install it separately.
-unittest.mock: This library assists in creating mocks and advanced test development. Like unittest, it comes bundled with Python, so there's no need to install it separately.
"""

# Import necessary libraries
import math
import sys
from collections import defaultdict
import random
import pyttsx3
from typing import List, Tuple, Optional
import tkinter as tk
from playerNamesScreen import PlayerNamesScreen
from gameOpeningScreen import GameOpeningScreen
from tkinter import messagebox, ttk
from player import Player
from tkinter import Toplevel, Button, Label
import winsound
import os
from datetime import datetime
Coordinates=Tuple[int,int]
NUM_ROWS = 17
NUM_COLUMNS = 25


class Game:
    def __init__(self) -> None:
        """
        Initialize the game.

        Attributes:
            __players (list): List to store player objects.
            current_player_index (int): Index of the current player.
            log (list): List to store game log.
            __num_players (int): Number of players in the game.
            __board_of_buttons (list): List to store buttons representing the game board.
            __board_coord (list): List to store coordinates of buttons on the game board.
            __current_colors_coord (defaultdict): Dictionary to store coordinates for each color.
            __root (tk.Tk): Root window of the game.
            colors (list): List of color options for players.
            __current_turn (int): Current turn count.
            engine (pyttsx3.engine.Engine): Text-to-speech engine.
            __during_turn (bool): Flag indicating whether it's during a player's turn.
            current_turn_possible_moves (list): List to store possible moves during a turn.
            __current_coord_to_move (tuple): Coordinates of the current piece to move.
            __current_btn_to_move (tk.Button): Button representing the current piece to move.
            __new_game_new_start (bool): Flag indicating whether it's a new game or a new start.
            against_comp (bool): Flag indicating whether the game is against the computer.
            comp_turn (bool): Flag indicating whether it's the computer's turn.
            __current_comp_btn (tk.Button): Button representing the current piece for the computer's turn.
            __current_comp_coord (tuple): Coordinates of the current piece for the computer's turn.
            current_datetime (str): Current date and time formatted as "YYYY-MM-DD_HH-MM-SS".
            file_name (str): File name for storing the game log.
            log_file_path (str): File path for storing the game log.
            __hard_level (bool): Flag indicating whether the game is set to hard level when playing against the computer.
        """
        self.__players=[]
        self.current_player_index = 0
        self.log = []
        self.__num_players =0
        self.__board_of_buttons = []
        self.__board_coord = []
        self.__current_colors_coord = defaultdict(list)
        self.__root=None
        self.colors=["blue", "yellow", "red", "green", "purple", "orange"]
        self.__current_turn=0
        self.engine = pyttsx3.init()
        self.__during_turn=False
        self.current_turn_possible_moves=[]
        self.__current_coord_to_move=()
        self.__current_btn_to_move = None
        self.__new_game_new_start=False
        self.against_comp=False
        self.comp_turn=False
        self.__current_comp_btn=None
        self.__current_comp_coord=()
        self.current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.file_name=f"game_log_{self.current_datetime}.txt"
        self.log_file_path = os.path.join(os.path.dirname(__file__), f"game_log_{self.current_datetime}.txt")
        self.__hard_level = False

    def show_rules(self) -> None:
        """
        Display the rules of the game to the players.

        This method prompts the players if they want to see the rules of the game.
        If they choose to see the rules, the rules are displayed in a message box.

        Rules of the Game:
        1. Each player takes turns selecting a square they wish to move. The game highlights possible moves for the player in pink. Once a square is selected, it cannot be chosen again if a valid move is already made.
        2. At the top of the window, the current player's turn is indicated along with their color. Additionally, a sound plays to signify whose turn it is.
        3. The game concludes when a player of any other color enters one of the players' territories.
        4. If players wish to replay with the same lineup, they must respond "yes" twice to the prompts that appear after the results are presented.
        5. If players desire to play again with a different team, they should select "yes" and then "no" when prompted.
        """
        try:
            response = messagebox.askyesno("Rules", "Would you like to see the rules of the game before we start?")
        except:
            messagebox.showerror("Error", "An error occurred while displaying the rules.")
            return

        if response:
            try:
                rules_of_the_game = """
                Rules of the Game:

                1. Each player takes turns selecting a square they wish to move. The game highlights possible moves for the player in pink. Once a square is selected, it cannot be chosen again if a valid move is already made.

                2. At the top of the window, the current player's turn is indicated along with their color. Additionally, a sound plays to signify whose turn it is.

                3. The game concludes when a player of any other color enters one of the players' territories.

                4. If players wish to replay with the same lineup, they must respond "yes" twice to the prompts that appear after the results are presented.

                5. If players desire to play again with a different team, they should select "yes" and then "no" when prompted.
                """
                messagebox.showinfo("Rules", rules_of_the_game)
            except:
                messagebox.showerror("Error", "An error occurred while displaying the rules.")
                return
        messagebox.showinfo("Have fun!")

    def create_board(self, num_of_players: int) -> None:
        """
        Create the Chinese Checkers board layout with buttons.
        """
        try:
            self.__root = tk.Tk()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the game board: {str(e)}")
            return

        # Define colors for different player zones
        colors = self.colors
        # Define positions for each player
        positions = [
            [(0, 12), (1, 11), (1, 13), (2, 10), (2, 12), (2, 14), (3, 9), (3, 11), (3, 13), (3, 15)],
            [(16, 12), (15, 11), (15, 13), (14, 10), (14, 14), (14, 12), (13, 9), (13, 11), (13, 13), (13, 15)],
            [(9, 3), (10, 2), (10, 4), (11, 1), (11, 3), (11, 5), (12, 0), (12, 2), (12, 4), (12, 6)],
            [(7, 3), (6, 2), (6, 4), (5, 1), (5, 3), (5, 5), (4, 0), (4, 2), (4, 4), (4, 6)],
            [(9, 21), (10, 20), (10, 22), (11, 19), (11, 21), (11, 23), (12, 18), (12, 20), (12, 22), (12, 24)],
            [(7, 21), (6, 20), (6, 22), (5, 19), (5, 21), (5, 23), (4, 18), (4, 20), (4, 22), (4, 24)]
        ]

        # Determine the number of colorful triangles based on the number of players
        num_colorful_triangles = min(num_of_players, len(colors))

        try:
            # Create buttons for each player's positions
            for i in range(num_colorful_triangles):
                for p in positions[i]:
                    if p not in self.__board_coord:  # Check if the position is not already occupied by a button
                        try:
                            button = tk.Button(self.__root, text="", width=2, bg=colors[i])
                            button.grid(row=p[0], column=p[1])
                            button.bind("<Button-1>",
                                        lambda event, row=p[0], col=p[1]: self.handle_button_click(row,
                                                                                                   col))  # Bind the button click event
                            self.__board_of_buttons.append(button)
                            self.__board_coord.append(p)
                            self.__current_colors_coord[colors[i]].append(p)
                        except Exception as e:
                            messagebox.showerror("Error", f"An error occurred while creating a button: {str(e)}")
                            return

            # Create additional buttons for special conditions
            for color in [0, 3]:
                for coord in positions[color]:
                    for i in range(11):
                        # Check if the position is not occupied by any player and is in the base area
                        if (coord[0] + i, coord[1] + i) not in sum(positions, []):
                            if self.is_button_in_base(coord[0] + i, coord[1] + i):
                                if (coord[0] + i, coord[
                                                      1] + i) not in self.__board_coord:  # Check if the position is not already occupied by a button
                                    try:
                                        button = tk.Button(self.__root, text="", width=2, bg="white")
                                        button.grid(row=coord[0] + i, column=coord[1] + i)
                                        button.bind("<Button-1>",
                                                    lambda event, row=coord[0] + i,
                                                           col=coord[1] + i: self.handle_button_click(
                                                        row, col))  # Bind the button click event
                                        self.__board_of_buttons.append(button)
                                        self.__board_coord.append((coord[0] + i, coord[1] + i))
                                    except Exception as e:
                                        messagebox.showerror("Error",
                                                             f"An error occurred while creating a button: {str(e)}")
                                        return

            # Create additional buttons for the center area
            for i in range(9):
                row_val = 4 + i
                col_val = 8 + i
                if (
                        row_val,
                        col_val) not in self.__board_coord:  # Check if the position is not already occupied by a button
                    try:
                        button = tk.Button(self.__root, text="", width=2, bg="white")
                        button.grid(row=row_val, column=col_val)
                        button.bind("<Button-1>",
                                    lambda event, row=row_val, col=col_val: self.handle_button_click(row,
                                                                                                     col))  # Bind the button click event
                        self.__board_coord.append((row_val, col_val))
                        self.__board_of_buttons.append(button)
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while creating a button: {str(e)}")
                        return
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the game board: {str(e)}")
            return

    def get_button_at_location(self, row: int, col: int) -> Optional[tk.Button]:
        """
        Get the button at a specific location on the board by row and column.

        Parameters:
            row (int): The row index of the button.
            col (int): The column index of the button.

        Returns:
            Optional[tk.Button]: The button at the specified location, or None if no button is found at that location.
        """
        try:
            # Iterate over all buttons and check their positions
            for button, (button_row, button_col) in zip(self.__board_of_buttons, self.__board_coord):
                # Check if the button's row and column match the given row and column
                if button_row == row and button_col == col:
                    return button
            # If no button matches the given row and column, return None
            return None
        except Exception as e:
            messagebox.showerror("Error",
                                 f"An error occurred while getting the button at location ({row}, {col}): {str(e)}")
            return None

    def get_button_color(self, button: tk.Button) -> str:
        """
        Get the color of a specific button.

        Parameters:
            button (tk.Button): The button object.

        Returns:
            str: The background color of the button.
        """
        try:
            # Retrieve the background color of the button
            color = button["bg"]
            return color
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while getting the color of the button: {str(e)}")
            return ""

    def set_button_color(self, button: tk.Button, new_color: str) -> None:
        """
        Change the color of a specific button.

        Parameters:
            button (tk.Button): The button object.
            new_color (str): The new background color for the button.
        """
        try:
            # Set the background color of the button to the new color
            button.configure(bg=new_color)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while setting the color of the button: {str(e)}")

    def is_button_in_base(self, row: int, col: int) -> bool:
        """
        Check if a button is in the base area of any player.

        Parameters:
            row (int): The row index of the button.
            col (int): The column index of the button.

        Returns:
            bool: True if the button is in the base area of any player, False otherwise.
        """
        try:
            # Check for base area boundaries for each player
            for i in range(4):
                if row == 4 + i and 7 - i < col < 17 + i:
                    return True
            for i in range(5):
                if row == 8 + i and 3 + i < col < 22 - i:
                    return True
            return False
        except Exception as e:
            messagebox.showerror("Error",
                                 f"An error occurred while checking if the button is in the base area: {str(e)}")
            return False


    def calculate_possible_moves(self, current_row: int, current_col: int) -> List[Coordinates]:
        """
        Calculates all possible moves from the given button coordinates.

        Args:
            current_row (int): The row of the current button.
            current_col (int): The column of the current button.

        Returns:
            List[Coordinates]: A list of coordinates representing possible moves.
        """
        possible_moves = []
        visited = defaultdict(bool)  # Dictionary to track visited buttons

        # Define a recursive function to explore diagonal jumps
        def explore_diagonals(row: int, col: int, direction: Tuple[int, int], prev_color: str) -> None:
            """
            Recursive function to explore diagonal jumps.

            Args:
                row (int): The current row.
                col (int): The current column.
                direction (Tuple[int, int]): The direction to explore.
                prev_color (str): The color of the previously visited button.
            """
            try:
                # Calculate the next button coordinates in the given direction
                next_row = row + direction[0]
                next_col = col + direction[1]

                # Get the button at the next coordinates
                next_button = self.get_button_at_location(next_row, next_col)
                if next_button is not None:  # Ensure the button exists
                    # Get the color of the next button
                    next_color = self.get_button_color(next_button)
                    # Check if the next button is empty or the same color as the previous one
                    if next_color == "white" or next_color == prev_color:
                        # Explore further in the same direction
                        explore_diagonals(next_row, next_col, direction, prev_color)
                    elif next_color != prev_color:
                        # If the next button is a different color and the button beyond it is white, it's a possible move
                        btn_after_next = self.get_button_at_location(next_row + direction[0], next_col + direction[1])
                        if btn_after_next is not None:
                            if self.get_button_color(btn_after_next) == "white":
                                possible_moves.append((next_row + direction[0], next_col + direction[1]))
                                # Explore further for double jumps
                                explore_diagonals(next_row + direction[0], next_col + direction[1], direction,
                                                  prev_color)
                    # Mark the current button as visited
                    visited[(row, col)] = True
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        # Define the directions for diagonal jumps
        directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]

        # Explore diagonal jumps in all directions
        for direction in directions:
            try:
                # Get the current button
                current_button = self.get_button_at_location(current_row, current_col)
                if current_button is not None:  # Ensure the button exists
                    # Get the color of the current button
                    current_color = self.get_button_color(current_button)
                    explore_diagonals(current_row, current_col, direction, current_color)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        # Return the list of possible moves
        four_direct=self.four_diag_white(current_row,current_col)
        return four_direct+possible_moves

    def four_diag_white(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Check diagonals from the given coordinate.

        Parameters:
            row (int): The row index of the coordinate.
            col (int): The column index of the coordinate.

        Returns:
            List[Tuple[int, int]]: A list of coordinates of white buttons in the four diagonal directions.
        """
        try:
            # Check upper left diagonal
            four_direc = []
            btn = self.get_button_at_location(row - 1, col - 1)
            if btn is not None:
                if self.get_button_color(btn) == "white":
                    four_direc.append((row - 1, col - 1))

            # Check upper right diagonal
            btn = self.get_button_at_location(row - 1, col + 1)
            if btn is not None:
                if self.get_button_color(btn) == "white":
                    four_direc.append((row - 1, col + 1))

            # Check lower left diagonal
            btn = self.get_button_at_location(row + 1, col - 1)
            if btn is not None:
                if self.get_button_color(btn) == "white":
                    four_direc.append((row + 1, col - 1))

            # Check lower right diagonal
            btn = self.get_button_at_location(row + 1, col + 1)
            if btn is not None:
                if self.get_button_color(btn) == "white":
                    four_direc.append((row + 1, col + 1))

            return four_direc
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking diagonals: {str(e)}")
            return []

    def show_custom_message(self, message: str) -> None:
        """
        Display a custom message in a popup window.

        Parameters:
            message (str): The message to be displayed in the popup window.
        """
        try:
            popup = Toplevel()
            popup.title("Wrong place")
            label = Label(popup, text=message)
            label.pack()
            button = Button(popup, text="OK", command=popup.destroy)
            button.pack()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying custom message: {str(e)}")

    def filter_coordinates(self, coordinates_list: List[Tuple[int, int]], reference_coord: Tuple[int, int]) -> List[
        Tuple[int, int]]:
        """
        This function takes a list of coordinates and an additional coordinate and returns a list with all coordinates smaller than the given coordinate.

        Parameters:
            coordinates_list (List[Tuple[int, int]]): The list of coordinates.
            reference_coord (Tuple[int, int]): The coordinate to compare to.

        Returns:
            List[Tuple[int, int]]: The list of coordinates smaller than the given coordinate.
        """
        try:
            filtered_coords = [coord for coord in coordinates_list if
                               coord[0] < reference_coord[0] and coord[1] < reference_coord[1]]
            return filtered_coords
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while filtering coordinates: {str(e)}")
            return []

    def distance(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> float:
        """
        Calculates the distance between two points.

        Parameters:
            coord1 (Tuple[int, int]): The coordinates of the first point.
            coord2 (Tuple[int, int]): The coordinates of the second point.

        Returns:
            float: The distance between the two points.
        """
        try:
            return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating distance: {str(e)}")
            return 0.0

    def closest_and_farthest_enemy_locations(self, enemy_coords: List[Tuple[int, int]],
                                             player_coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Returns a list of the closest and farthest locations from the enemy.

        Parameters:
            enemy_coords (List[Tuple[int, int]]): A list of enemy coordinates.
            player_coords (List[Tuple[int, int]]): A list of player coordinates.

        Returns:
            List[Tuple[int, int]]: A list containing the closest and farthest locations from the enemy.
        """
        try:
            min_distance = float('inf')
            max_distance = float('-inf')
            closest_locations = []
            farthest_locations = []

            # Calculate distances from each player coordinate to enemy coordinates
            distances = []
            for player_coord in player_coords:
                min_dist = float('inf')
                for enemy_coord in enemy_coords:
                    dist = self.distance(player_coord, enemy_coord)
                    if dist < min_dist:
                        min_dist = dist
                distances.append((player_coord, min_dist))

            # Sort the list by distance from smallest to largest
            distances.sort(key=lambda x: x[1])

            # Group of the closest locations
            closest_locations = [coord for coord, _ in distances]

            # Group of the farthest locations
            farthest_locations = [coord for coord, _ in reversed(distances)]

            return closest_locations + farthest_locations
        except Exception as e:
            messagebox.showerror("Error",
                                 f"An error occurred while calculating closest and farthest enemy locations: {str(e)}")
            return []

    def computer_move(self) -> None:
        """
        Performs a move for the computer player.

        This function first determines the move strategy based on the game's difficulty level.
        If the game is set to hard level, the computer player calculates the closest enemy locations
        and selects its move based on reaching the closest enemy. Otherwise, it chooses a random
        move from its available options.

        After determining the source and destination coordinates for the move, the function updates
        the GUI by changing the colors of the buttons representing the current and destination locations.

        Finally, the function updates the game state by moving the computer player's piece and logging the move.
        """
        try:
            comp_player = self.__players[self.current_player_index]

            if self.__hard_level:
                lst_of_closest_enemy = []
                # Find the closest enemy locations
                for coord in self.__players[0].get_player_home_locations():
                    current_btn = self.get_button_at_location(coord[0], coord[1])
                    color = self.get_button_color(current_btn)
                    if color == "white":
                        lst_of_closest_enemy = [coord]
                if lst_of_closest_enemy == []:
                    lst_of_closest_enemy = self.__players[0].get_player_home_locations()
                lst_of_coords_from_closest = self.closest_and_farthest_enemy_locations(lst_of_closest_enemy,
                                                                                       self.__players[
                                                                                           1].get_player_current_locations())
                current_coord = lst_of_coords_from_closest[0]
                possible_moves_per_current_coord = self.calculate_possible_moves(current_coord[0], current_coord[1])
                lst_from_closest_dest = self.closest_and_farthest_enemy_locations(lst_of_closest_enemy,
                                                                                  possible_moves_per_current_coord)
                dest_coord = lst_from_closest_dest[0]
                i = 0
                # Move towards the closest enemy location
                while dest_coord[0] > current_coord[0]:
                    i = i + 1
                    current_coord = lst_of_coords_from_closest[i]
                    possible_moves_per_current_coord = self.calculate_possible_moves(current_coord[0], current_coord[1])
                    lst_from_closest_dest = self.closest_and_farthest_enemy_locations(
                        self.__players[0].get_player_home_locations(), possible_moves_per_current_coord)
                    if lst_from_closest_dest != []:
                        dest_coord = lst_from_closest_dest[0]
                    if i == len(lst_of_coords_from_closest) - 1:
                        i = 0
            else:
                # Randomly choose a move from available options
                current_coord = random.choice(comp_player.get_player_current_locations())
                comp_possible_moves = self.calculate_possible_moves(current_coord[0], current_coord[1])
                while comp_possible_moves == [] or self.filter_coordinates(comp_possible_moves, current_coord) == []:
                    current_coord = random.choice(comp_player.get_player_current_locations())
                    comp_possible_moves = self.calculate_possible_moves(current_coord[0], current_coord[1])
                dest_coord = random.choice(self.filter_coordinates(comp_possible_moves, current_coord))

            # Update GUI with button color changes
            current_btn = self.get_button_at_location(current_coord[0], current_coord[1])
            dest_btn = self.get_button_at_location(dest_coord[0], dest_coord[1])
            self.set_button_color(current_btn, "white")
            self.set_button_color(dest_btn, self.__players[self.current_player_index].get_color())

            # Move the computer player's piece and log the move
            comp_player.move_coord(current_coord, dest_coord)
            self.log_move(self.__players[self.current_player_index].get_name(),
                          self.__players[self.current_player_index].get_color(),
                          f"Selected piece at ({current_coord[0]}, {current_coord[1]})",
                          dest_coord)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during computer move: {str(e)}")

    def player_against_comp_move(self, row: int, col: int) -> None:
        """
        Executes a move when playing against the computer.

        Parameters:
            row (int): The row index of the selected button.
            col (int): The column index of the selected button.

        This function handles the player's move when playing against the computer. It first checks if the selected button
        belongs to the player's color. If so, it proceeds with the move selection process.

        During the player's turn, the function allows the player to select a piece to move and highlights the available
        destination options. Once the player confirms the move, it validates the destination and executes the move if it's
        valid. It then logs the move and switches to the computer player's turn.

        If the player wins or loses after the move, the function updates player stats, displays the game results, and
        switches to the next player's turn (either human or computer). If there is a winner after the computer player's
        turn, it displays the game results accordingly.
        """
        try:
            if self.get_button_color(self.get_button_at_location(row, col)) in ["blue", "magenta"]:
                if not self.__during_turn:
                    self.__current_btn_to_move = self.get_button_at_location(row, col)
                    self.__current_coord_to_move = (row, col)
                    self.current_turn_possible_moves = self.calculate_possible_moves(row, col)
                    if self.current_turn_possible_moves == []:
                        self.show_custom_message("There's no options to move from here, try another place")
                        return
                    for coord in self.current_turn_possible_moves:
                        btn = self.get_button_at_location(coord[0], coord[1])
                        self.set_button_color(btn, "magenta")
                    self.__during_turn = not self.__during_turn
                else:
                    dest_btn = self.get_button_at_location(row, col)
                    if self.get_button_color(dest_btn) == "magenta":
                        # Move the piece to the selected destination if it's a valid move
                        self.set_button_color(dest_btn, self.colors[self.current_player_index])
                        for coord in self.current_turn_possible_moves:
                            btn = self.get_button_at_location(coord[0], coord[1])
                            if self.get_button_color(btn) == "magenta":
                                self.set_button_color(btn, "white")
                        self.log_move(self.__players[self.current_player_index].get_name(),
                                      self.__players[self.current_player_index].get_color(),
                                      f"Selected piece at ({self.__current_coord_to_move[0]}, {self.__current_coord_to_move[1]})",
                                      (row, col))
                        self.set_button_color(self.__current_btn_to_move, "white")
                        self.__during_turn = not self.__during_turn
                        if self.is_winner():
                            self.win_sound()
                            # Update players' stats accordingly
                            self.__players[self.current_player_index].update_stats("win")
                            for player in self.__players:
                                if player is not self.__players[self.current_player_index]:
                                    player.update_stats("loss")
                            with open("game_log.txt", "a") as log_file:
                                log_file.write(
                                    "The winner is: " + self.__players[self.current_player_index].get_name() + "\n")
                            # Display game results
                            self.display_game_results()
                        # Switch to the next player's turn
                        if self.current_player_index == self.__num_players - 1:
                            self.current_player_index = 0
                        else:
                            self.current_player_index += 1
                        self.computer_move()
                        # Check if there's a winner after the move
                        if self.is_winner():
                            self.win_sound()
                            # Update players' stats accordingly
                            self.__players[self.current_player_index].update_stats("win")
                            for player in self.__players:
                                if player is not self.__players[self.current_player_index]:
                                    player.update_stats("loss")
                            # Display game results
                            self.display_game_results()
                        # Switch to the next player's turn
                        if self.current_player_index == self.__num_players - 1:
                            self.current_player_index = 0
                        else:
                            self.current_player_index += 1
                    else:
                        # Show a message if the selected destination is not valid
                        self.wrong_sound()
                        self.show_custom_message(
                            "The place is not available. Note that you select a button from the suggested buttons")
            else:
                self.show_custom_message(
                    "You can click only your buttons!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during player move: {str(e)}")

    def log_move(self, player_name: str, color: str, selected_button: str, destination_button: str) -> None:
        """
        Logs a player's move to a file.

        Parameters:
            player_name (str): The name of the player making the move.
            color (str): The color of the player's piece.
            selected_button (str): The button selected by the player to move from.
            destination_button (str): The destination button selected by the player.

        This function logs the details of a player's move, including their name, piece color, the button they selected as
        the starting point, and the destination button they moved to. It appends this information to a log file for
        reference and analysis.
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
            with open(self.file_name, "a") as log_file:
                log_file.write(
                    f"{timestamp} - Player: {player_name}. Color: {color}. Selected button: {selected_button}. Destination button: {destination_button}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while logging the move: {str(e)}")
        # try:
        #     with open(self.file_name, "a") as log_file:
        #         log_file.write(
        #             f"Player: {player_name}. Color: {color}. Selected button: {selected_button}. Destination button: {destination_button}\n")
        # except Exception as e:
        #     messagebox.showerror("Error", f"An error occurred while logging the move: {str(e)}")

    def handle_button_click(self, row: int, col: int) -> None:
        """
        Handle button click event.

        If playing against the computer, execute the appropriate move.
        Otherwise, handle the button click for human players.

        Parameters:
            row (int): The row index of the clicked button.
            col (int): The column index of the clicked button.

        This function handles the button click event. If the game is set to play against the computer, it executes the
        appropriate move. Otherwise, it handles the button click for human players.

        During a player's turn, the function allows the player to select a piece to move and highlights the available
        destination options. Once the player confirms the move, it validates the destination and executes the move if it's
        valid. It then logs the move and switches to the next player's turn.

        If there is a winner after the move, the function updates player stats, displays the game results, and switches to
        the next player's turn. If the game is played against the computer, it also announces the next player's turn.

        """
        try:
            if self.against_comp:  # Check if playing against the computer
                self.player_against_comp_move(row, col)  # Execute the move for player against computer
            else:
                if not self.__during_turn:  # Check if it's not currently any player's turn
                    # Check if it's the current player's turn
                    self.__current_btn_to_move = self.get_button_at_location(row, col)
                    if self.get_button_color(self.__current_btn_to_move) != self.colors[self.current_player_index]:
                        # Show a message if it's not the current player's turn
                        self.show_custom_message(
                            "It's not your turn! It's " + self.__players[self.current_player_index].get_name() +
                            ", color: " + self.colors[self.current_player_index])
                    else:
                        # Get possible moves for the selected piece and mark them on the board
                        self.__current_coord_to_move = (row, col)
                        self.current_turn_possible_moves = self.calculate_possible_moves(row, col)
                        if self.current_turn_possible_moves == []:
                            self.show_custom_message("There's no options to move from here, try another place")
                            return
                        for coord in self.current_turn_possible_moves:
                            btn = self.get_button_at_location(coord[0], coord[1])
                            self.set_button_color(btn, "magenta")
                        self.__during_turn = not self.__during_turn
                else:
                    # Handle player's move during their turn
                    dest_btn = self.get_button_at_location(row, col)
                    if self.get_button_color(dest_btn) == "magenta":
                        # Move the piece to the selected destination if it's a valid move
                        self.set_button_color(dest_btn, self.colors[self.current_player_index])
                        for coord in self.current_turn_possible_moves:
                            btn = self.get_button_at_location(coord[0], coord[1])
                            if self.get_button_color(btn) == "magenta":
                                self.set_button_color(btn, "white")
                        self.log_move(self.__players[self.current_player_index].get_name(),
                                      self.__players[self.current_player_index].get_color(),
                                      f"Selected piece at ({self.__current_coord_to_move[0]}, {self.__current_coord_to_move[1]})",
                                      (row, col))
                        self.set_button_color(self.__current_btn_to_move, "white")
                        self.__during_turn = not self.__during_turn
                        # Switch to the next player's turn
                        if self.current_player_index == self.__num_players - 1:
                            self.current_player_index = 0
                        else:
                            self.current_player_index += 1
                        # Check if there's a winner after the move
                        if self.is_winner():
                            self.win_sound()
                            # Update players' stats accordingly
                            self.__players[self.current_player_index].update_stats("win")
                            for player in self.__players:
                                if player is not self.__players[self.current_player_index]:
                                    player.update_stats("loss")
                            with open("game_log.txt", "a") as log_file:
                                log_file.write(
                                    "The winner is: " + self.__players[self.current_player_index].get_name() + "\n")
                            # Display game results
                            self.display_game_results()
                        message = "It's " + self.__players[self.current_player_index].get_name() + ", color: " + \
                                  self.colors[self.current_player_index]
                        self.__root.title(message)
                        message_voice = "It's " + self.__players[
                            self.current_player_index].get_name() + "turn,your color is: " + self.colors[
                                            self.current_player_index]
                        self.next_turn_sound(message_voice)
                    else:
                        # Show a message if the selected destination is not valid
                        self.wrong_sound()
                        self.show_custom_message(
                            "The place is not available. Note that Note that you select a button from the suggested buttons")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while handling button click: {str(e)}")

    def display_game_results(self) -> None:
        """
        Display the results of the game in a graphical window.

        This function creates a new graphical window displaying the results of the game. It shows the winner(s) and their
        number of wins, as well as the wins and losses for other players.

        """
        try:
            # Create a new graphical window
            root2 = tk.Tk()
            root2.title("Game Results")
            root2.geometry("500x500")  # Set window size
            root2.configure(bg="lightblue")  # Set background color for the window

            # Style configurations
            style = ttk.Style()
            style.configure("Title.TLabel", font=("Arial", 25, "bold"), foreground="white",
                            background="lightblue")  # Style for the title
            style.configure("Winner.TLabel", font=("Arial", 20, "bold"), foreground="red",
                            background="lightblue")  # Style for the winner label
            style.configure("Player.TLabel", font=("Arial", 20), foreground="black",
                            background="lightblue")  # Style for player labels

            # Adding a title inside the window
            title_label = ttk.Label(root2, text="Game Results", style="Title.TLabel")
            title_label.pack(pady=10)

            # Divide players into winners and others
            winners = [player for player in self.__players if player.get_wins() > 0]
            others = [player for player in self.__players if player not in winners]

            # Display the winner(s) and their wins
            if winners:
                winner_text = f"Winner(s): {', '.join([winner.get_name() for winner in winners])}, won with {winners[0].get_wins()} wins"
                winner_label = ttk.Label(root2, text=winner_text, style="Winner.TLabel")
                winner_label.pack(pady=5)

            # Adding a results table for the other players
            for i, player in enumerate(others, start=len(winners) + 1):
                player_label = ttk.Label(root2,
                                         text=f"{player.get_name()}: Wins - {player.get_wins()}, Losses - {player.get_losses()}",
                                         style="Player.TLabel")
                player_label.pack(pady=5, anchor="w")

            # Display the window
            root2.after(5000, self.close_window, root2)  # Close the window after 5 seconds
            root2.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying game results: {str(e)}")

    def close_window(self, root: tk.Tk) -> None:
        """
        Close the given window.

        This function closes the specified graphical window.

        Args:
            root (tk.Tk): The Tkinter root window to be closed.
        """
        try:
            root.destroy()
            self.if_play_again()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while closing the window: {str(e)}")

    def win_sound(self) -> None:
        """
        Play a winning sound effect.

        This function plays a sequence of beeps to indicate winning.

        """
        try:
            winsound.Beep(800, 200)
            winsound.Beep(900, 200)
            winsound.Beep(1000, 200)
            winsound.Beep(800, 500)
            winsound.Beep(600, 700)
        except Exception as e:
            print(f"An error occurred while playing the winning sound: {e}")

    def wrong_sound(self) -> None:
        """
        Play a sound effect indicating an incorrect action.

        This function plays a sequence of beeps to indicate an incorrect action.

        """
        try:
            winsound.Beep(150, 200)
            winsound.Beep(200, 200)
            winsound.Beep(300, 200)
            winsound.Beep(200, 600)
        except Exception as e:
            print(f"An error occurred while playing the wrong sound: {e}")

    def next_turn_sound(self, current_message: str) -> None:
        """
        Play a sound effect and announce the next player's turn.

        This function utilizes text-to-speech to announce the next player's turn and updates the window title accordingly.

        Args:
            current_message (str): The message to be announced.

        """
        try:
            self.engine.say(current_message)
            self.engine.runAndWait()
            self.__root.title(current_message)
        except Exception as e:
            print(f"An error occurred during announcing next turn: {e}")

    def is_winner(self) -> bool:
        """
        Check if there is a winner in the game.

        This function checks if any player has successfully moved all their pieces to their respective home locations.

        Returns:
            bool: True if there is a winner, False otherwise.

        """
        for player in self.__players:
            for coord in player.get_player_home_locations():
                try:
                    btn = self.get_button_at_location(coord[0], coord[1])
                    if self.get_button_color(btn) != player.get_color() and self.get_button_color(btn) != "white":
                        return True
                except Exception as e:
                    print(f"Error checking button color at location {coord}: {e}")
        return False

    def bind_button_clicks(self) -> None:
        """
        Bind button clicks to the handle_button_click method.

        This function iterates through all buttons on the board and binds the <Button-1> event to the handle_button_click method,
        ensuring that when a button is clicked, the appropriate action is taken.

        """
        for current_row in range(NUM_ROWS):
            for current_col in range(NUM_COLUMNS):
                button = self.get_button_at_location(current_row, current_col)
                if button:
                    try:
                        # Bind the <Button-1> event to the handle_button_click method
                        button.bind("<Button-1>",
                                    lambda event, row=current_row, col=current_col: self.handle_button_click(row, col))
                    except Exception as e:
                        print(f"Error binding event for button at row {current_row}, column {current_col}: {e}")

    def prep_game(self):
        """
            Prepares the game by initializing the game setup based on user inputs.
            This includes creating the game board, setting up player positions, and other game configurations.

        """
        try:
            opening_screen = GameOpeningScreen()
            file_name = opening_screen.get_file()
            play_against_computer = opening_screen.is_player_against_comp()
            if file_name != "":
                self.file_name = file_name
                with open(file_name, 'r') as file:
                    first_line = file.readline()
                    # Reading the second line
                    second_line = file.readline()
                    self.__num_players = int(second_line[:-1])
                    self.create_board(self.__num_players)
                    lines = file.readlines()
                    players_names_lst = []
                    # Loop through each line in the lines list
                    for line in lines:
                        # Check if the line starts with "Player"
                        if line.startswith("Player"):
                            # Extract details from the current line
                            split_line = line.split(". ")
                            name = split_line[0].split(": ")[1]
                            if name not in players_names_lst:
                                players_names_lst.append(name)
                            color = split_line[1].split(": ")[1]
                            current_coord = split_line[2].split(": ")[1]
                            opening_index = current_coord.find('(')
                            last_to_specific_char = current_coord[opening_index:]
                            dest_coord = split_line[3].split(": ")[1][:-1]
                            opening_index = dest_coord.find('(')
                            last_to_specific_char_d = dest_coord[opening_index:]
                            current_coord = tuple(map(int, last_to_specific_char.strip("()").split(", ")))
                            dest_coord = tuple(map(int, last_to_specific_char_d.strip("()").split(", ")))
                            print(current_coord[0])
                            current_btn = self.get_button_at_location(current_coord[0], current_coord[1])
                            self.set_button_color(current_btn, "white")
                            dest_btn = self.get_button_at_location(dest_coord[0], dest_coord[1])
                            self.set_button_color(dest_btn, color)
                        for i, player_name in enumerate(players_names_lst):
                            # Create a player object for each player name using the corresponding color
                            self.__players.append(
                                Player(self.colors[i], self.__current_colors_coord[self.colors[i]], player_name))
            else:
                self.__num_players = opening_screen.get_num_players()
                with open(self.file_name, "a") as log_file:
                    log_file.write("Chinese checkers by Naama Even Oz - Game Log\n")
                    log_file.write(str(self.__num_players) + "\n")
                self.__num_players = opening_screen.get_num_players()
                if play_against_computer != 0:
                    if play_against_computer == 2:
                        self.__hard_level = True
                    self.against_comp = True
                    players_names_screen = PlayerNamesScreen(1)
                    player_name = players_names_screen.get_player_names()
                    self.create_board(2)
                    player_coords = self.__current_colors_coord["blue"]
                    comp_player_coords = self.__current_colors_coord["yellow"]
                    self.__players.append(Player(self.colors[0], player_coords, player_name[0]))
                    self.__players.append(Player(self.colors[1], comp_player_coords, "Computer"))
                else:
                    # Start game with selected number of local players
                    players_names_screen = PlayerNamesScreen(self.__num_players)
                    players_names_lst = players_names_screen.get_player_names()
                    self.create_board(self.__num_players)
                    for i, player_name in enumerate(players_names_lst):
                        # Create a player object for each player name using the corresponding color
                        self.__players.append(
                            Player(self.colors[i], self.__current_colors_coord[self.colors[i]], player_name))

            # Log the start time of the game prep
            with open(self.file_name, "a") as log_file:
                log_file.write(f"Game preparation started at: {datetime.now()}\n")

        except Exception as e:
            print(f"An error occurred during game preparation: {e}")

    def if_play_again(self) -> None:
        """
        Prompt the user to play again.

        This function prompts the user with a message box asking if they want to play again. If the user chooses to play
        again, it then asks if they want to start a new game with the same players or with new players. Based on the user's
        choices, it either restarts the game with the same or new players or sets a flag for starting a new game with new
        players.

        """
        try:
            play_again = messagebox.askyesno("Play again?")

            if play_again:
                same_players = messagebox.askyesno("Same players or new game?")
                if same_players:
                    # Restart the game with the same players
                    self.__root.destroy()
                    self.current_player_index = 0
                    self.log = []
                    self.__board_of_buttons = []
                    self.__board_coord = []
                    self.__current_colors_coord = defaultdict(list)
                    self.__root = None
                    self.__current_turn = 0
                    self.__during_turn = False
                    self.current_turn_possible_moves = []
                    self.__current_coord_to_move = ()
                    self.__current_btn_to_move = None
                    self.create_board(self.__num_players)
                    current_message = "it's " + self.__players[0].get_name() + " turn. Your color is: " + self.colors[0]
                    self.engine.say(current_message)
                    self.engine.runAndWait()
                    if self.against_comp:
                        self.__players[1].reset_current_locations()
                    self.__root.mainloop()
                else:
                    # Set a flag for starting a new game with new players
                    self.__root.destroy()
                    self.__new_game_new_start = True
            else:
                self.__root.destroy()
                return
        except Exception as e:
            print(f"An error occurred while prompting to play again: {e}")

    def is_new_game_new_start(self) -> bool:
        """
        Check if the user opted for a new game with new players.

        Returns:
            bool: True if the user chose to start a new game with new players, False otherwise.

        """
        try:
            return self.__new_game_new_start
        except Exception as e:
            print(f"An error occurred while checking if it's a new game with new players: {e}")
            return False  # Or handle the error in some other way

    def start(self):
        """
        Start the Chinese checkers game.

        Prepares the game, shows the rules, announces the current player's turn, and starts the main loop of the game.

        """
        self.prep_game()  # Prepare the game, including setting up players and board
        self.show_rules()
        with open(self.file_name, "a") as log_file:
            log_file.write(
                "Chinese checkers by Naama Even Oz - Game Log\n")
        # Show the rules of the game to the players
        # current_message = "It's " + self.__players[0].get_name() + "'s turn. Your color is: " + self.colors[0]
        # self.engine.say(current_message)  # Announce the current player's turn using text-to-speech
        # self.engine.runAndWait()  # Run the text-to-speech engine to announce the current player's turn
        self.__root.mainloop()  # Start the main loop of the game


# Main entry point
if __name__ == "__main__":
    # Example usage:
    # board=Board()
    if len(sys.argv)>=2:
        rules_of_the_game = """
                        Rules of the Game:

                        1. Each player takes turns selecting a square they wish to move. The game highlights possible moves for the player in pink. Once a square is selected, it cannot be chosen again if a valid move is already made.

                        2. At the top of the window, the current player's turn is indicated along with their color. Additionally, a sound plays to signify whose turn it is.

                        3. The game concludes when a player of any other color enters one of the players' territories.

                        4. If players wish to replay with the same lineup, they must respond "yes" twice to the prompts that appear after the results are presented.

                        5. If players desire to play again with a different team, they should select "yes" and then "no" when prompted.
                        """
        if sys.argv[1]=="--help":
            print(rules_of_the_game)
    game = Game()
    game.start()
    if game.is_new_game_new_start():
        game = Game()
        game.start()



