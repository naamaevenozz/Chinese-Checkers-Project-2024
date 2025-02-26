import os
import tkinter as tk
from tkinter import filedialog, messagebox
import re


class GameOpeningScreen:
    def __init__(self) -> None:
        """
        Initializes the GameOpeningScreen object.
        """
        try:
            self.level_selected = 0
            self.filename = ""

            self.root = tk.Tk()
            self.root.title("Chinese Checkers - Opening Screen")
            self.root.configure(bg="lightblue")
            self.root.geometry("500x500")

            self.choice_made = False

            self.file_label = tk.Label(self.root, text="Select previous game file (if any):", bg="lightblue", fg="white",
                                       font=("Arial", 14))
            self.file_label.pack(pady=10)

            self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_file, bg="white", fg="blue",
                                           font=("Arial", 12))
            self.browse_button.pack()

            self.num_players_label = tk.Label(self.root, text="Select number of players (2-6):", bg="lightblue", fg="white",
                                              font=("Arial", 14))
            self.num_players_label.pack(pady=10)

            self.num_players_var = tk.IntVar(self.root)
            self.num_players_var.set(2)
            self.num_players_menu = tk.OptionMenu(self.root, self.num_players_var, *[i for i in range(2, 7)],
                                                  command=self.handle_num_players_choice)
            self.num_players_menu.config(bg="white", fg="blue", font=("Arial", 12))
            self.num_players_menu.pack()

            self.level_var = tk.StringVar()
            self.level_var.set("")
            self.level_1_radio = tk.Radiobutton(self.root, text="Level 1", variable=self.level_var, value="level_1",
                                                bg="lightblue", fg="white", font=("Arial", 12))
            self.level_1_radio.pack()
            self.level_2_radio = tk.Radiobutton(self.root, text="Level 2", variable=self.level_var, value="level_2",
                                                bg="lightblue", fg="white", font=("Arial", 12))
            self.level_2_radio.pack()

            self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, bg="white", fg="blue",
                                          font=("Arial", 12), state=tk.DISABLED)
            self.start_button.pack(pady=20)

            self.reset_button = tk.Button(self.root, text="Reset Choices", command=self.reset_choices, bg="white",
                                          fg="blue", font=("Arial", 12))
            self.reset_button.pack(pady=10)

            self.play_against_computer_var = tk.StringVar()
            self.play_against_computer_var.set("no")
            self.play_against_computer_yes_radio = tk.Radiobutton(self.root, text="Yes",
                                                                  variable=self.play_against_computer_var, value="yes",
                                                                  bg="lightblue", fg="white", font=("Arial", 12))
            self.play_against_computer_yes_radio.pack()

            self.play_against_computer_yes_radio.bind("<Button-1>", self.handle_choice)
            self.level_1_radio.bind("<Button-1>", self.handle_choice)
            self.level_2_radio.bind("<Button-1>", self.handle_choice)

            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def handle_choice(self, event) -> None:
        """
        Handles the selection made by the user.

        Args:
            event: The event object triggered by the user's selection.
        """
        if not self.choice_made:
            self.start_button.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.DISABLED)
            self.num_players_menu.config(state=tk.DISABLED)
            self.choice_made = True

    def handle_num_players_choice(self, value) -> None:
        """
        Handles the selection of number of players by the user.

        Args:
            value: The value selected by the user.
        """
        if not self.choice_made:
            self.browse_button.config(state=tk.DISABLED)
            self.play_against_computer_yes_radio.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)

    def validate_file(self, filename: str) -> bool:
        """
        Validates the selected file.

        Args:
            filename (str): The name of the file to be validated.

        Returns:
            bool: True if the file is valid, False otherwise.
        """
        try:
            if not os.path.isfile(filename):
                return False

            name, extension = os.path.splitext(filename)
            if extension.lower() != '.txt':
                return False

            agreed_line = "Chinese checkers by Naama Even Oz - Game Log"
            with open(filename, 'r') as file:
                first_line = file.readline().strip()
                if first_line != agreed_line:
                    return False

            return True
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return False

    def browse_file(self) -> None:
        """
        Opens a file dialog for selecting a file.
        """
        try:
            self.filename = filedialog.askopenfilename()

            if self.filename:
                if self.validate_file(self.filename):
                    print(f"Selected file: {self.filename}")
                    self.start_button.config(state=tk.NORMAL)
                else:
                    messagebox.showerror("Error", "Please select a valid text file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def start_game(self) -> int:
        """
        Starts the game with the selected options.

        Returns:
            int: The number of players for the game.
        """
        try:
            num_players = self.num_players_var.get()
            play_against_computer = self.play_against_computer_var.get()
            str_level_selected = self.level_var.get()
            if str_level_selected:
                self.level_selected = int(str_level_selected[-1])

            if num_players and play_against_computer:
                print(f"Starting game with {num_players} players.")

                if play_against_computer == "yes":
                    print("Playing against computer.")
                else:
                    print("Not playing against computer.")
            else:
                messagebox.showerror("Error", "Please make all selections before starting the game.")
            self.root.destroy()
            return num_players
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return 0

    def reset_choices(self) -> None:
        """
        Resets the choices made by the user.
        """
        self.browse_button.config(state=tk.NORMAL)
        self.play_against_computer_yes_radio.config(state=tk.NORMAL)
        self.num_players_menu.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.choice_made = False
        self.level_selected = 0
        self.filename = ""

    def get_screen_root(self) -> tk.Tk:
        """
        Gets the root window of the opening screen.

        Returns:
            tk.Tk: The root window of the opening screen.
        """
        return self.root

    def get_file(self) -> str:
        """
        Gets the filename selected by the user.

        Returns:
            str: The filename selected by the user.
        """
        return self.filename

    def get_num_players(self) -> int:
        """
        Gets the number of players selected by the user.

        Returns:
            int: The number of players selected by the user.
        """
        return self.num_players_var.get()

    def is_player_against_comp(self) -> int:
        """
        Checks if the player is playing against the computer.

        Returns:
            int: The level selected by the player for playing against the computer.
        """
        return self.level_selected
