import tkinter as tk
from tkinter import ttk
from vote import validate_voter, record_vote, get_csv_path


class VotingApp:
    """
    A graphical user interface (GUI) for the voting system.
    Requires the user to iput their voter ID and select a candidate before submitting their vote.
    """
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the voting application GUI.
        """
        self.root = root
        self.root.title("Voting System")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Voter ID Entry
        tk.Label(root, text="Voter ID:").pack(pady=5)
        self.voter_id_entry = tk.Entry(root, width=30)
        self.voter_id_entry.pack(pady=5)

        # Locks input to numeric values
        self.voter_id_entry.config(validate="key", validatecommand=(root.register(self.validate_numeric_input), "%P"))

        # Candidate Dropdown Menu
        tk.Label(root, text="Select Candidate:").pack(pady=5)
        self.candidate_var = tk.StringVar()
        self.candidate_dropdown = ttk.Combobox(
            root, textvariable=self.candidate_var, state="readonly", width=27
        )
        self.candidates = sorted(["John", "Jane"])
        self.candidate_dropdown['values'] = self.candidates
        self.candidate_dropdown.pack(pady=5)

        # Submit Button
        self.submit_button = tk.Button(root, text="Vote", command=self.vote)
        self.submit_button.pack(pady=10)

        # Message Label
        self.message_label = tk.Label(root, text="", fg="red", font=("Arial", 10))
        self.message_label.pack(pady=5)

    def validate_numeric_input(self, input_value: str) -> bool:
        """
        Validate that the input for Voter ID is numeric.
        """
        return input_value.isdigit() or input_value == ""

    def vote(self) -> None:
        """
        Handle the voting process after the "Vote" button is pressed.
        Validates voter ID, ensures a candidate is selected, and records the vote.
        """
        voter_id = self.voter_id_entry.get().strip()
        candidate = self.candidate_var.get()

        if not voter_id:
            self.message_label.config(text="Voter ID cannot be empty!", fg="red")
            return

        if not candidate:  # No candidate selected
            self.message_label.config(text="Please select a candidate!", fg="red")
            return

        if not validate_voter(voter_id, file_path=get_csv_path()):
            self.message_label.config(text="Voter ID already used! You cannot vote again.", fg="red")
            return

        # Record the vote
        record_vote(voter_id, candidate, file_path=get_csv_path())
        self.message_label.config(text=f"Vote recorded for {candidate}!", fg="green")
        self.voter_id_entry.delete(0, tk.END)
        self.candidate_var.set("")  # Reset the dropdown menu


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = VotingApp(root)
    root.mainloop()
