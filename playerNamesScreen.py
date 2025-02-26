import tkinter as tk
from tkinter import messagebox
import re
from typing import List

class PlayerNamesScreen:
    def __init__(self, num_players: int) -> None:
        """
        Initializes the PlayerNamesScreen object.

        Args:
            num_players (int): The number of players for whom names need to be entered.
        """
        try:
            self.num_players = num_players
            self.root = tk.Tk()
            self.root.title("Enter Player Names")
            self.root.geometry("500x500")
            self.root.configure(bg="lightblue")

            self.player_names: List[tk.Entry] = []

            for i in range(self.num_players):
                label = tk.Label(self.root, text=f"Player {i+1} Name:", bg="lightblue", font=("Verdana", 14))
                label.grid(row=i, column=0, padx=10, pady=10)

                entry = tk.Entry(self.root, font=("Verdana", 14))
                entry.grid(row=i, column=1, padx=10, pady=10)

                self.player_names.append(entry)

            submit_button = tk.Button(self.root, text="Submit", command=self.submit_names, bg="white", fg="blue", font=("Verdana", 14))
            submit_button.grid(row=self.num_players, columnspan=2, pady=20)
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def submit_names(self) -> None:
        """
        Submits the player names entered by the user.
        """
        try:
            names = [entry.get() for entry in self.player_names]
            if len(names) == len(set(names)):
                if all(re.match("^[a-zA-Z\s]*$", name) for name in names):
                    self.player_names = names
                    self.root.destroy()
                else:
                    messagebox.showerror("Invalid Names", "Please ensure that player names contain only English letters and spaces.")
            else:
                messagebox.showerror("Duplicate Names", "Please ensure that player names are unique.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_player_names(self) -> List[str]:
        """
        Returns the list of player names entered by the user.

        Returns:
            List[str]: A list containing the player names.
        """
        return self.player_names
