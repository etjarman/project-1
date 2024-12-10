import csv
import os
from typing import Optional


def get_csv_path(filename: str = "data.csv") -> str:
    """
    Get the file path to save the CSV file in the same directory.
    """
    return os.path.join(os.path.dirname(__file__), filename)


def vote_menu() -> str:
    """
    Display the voting menu and prompt the user for an option.
    """
    print('--------------------')
    print('VOTE MENU')
    print('--------------------')
    print('v: Vote')
    print('x: Exit')
    option = input('Option: ').lower().strip()
    while option != 'v' and option != 'x':
        option = input("Invalid (v/x): ").lower().strip()
    return option


def candidate_menu() -> int:
    """
    Display the candidate menu and prompt the user to select a candidate.
    """
    print('--------------------')
    print('CANDIDATE MENU')
    print('--------------------')
    print('1: John')
    print('2: Jane')
    vote = input('Candidate: ').strip()
    while vote != '1' and vote != '2':
        vote = input("Invalid (1/2): ").strip()
    return int(vote)


def validate_voter(voter_id: str, file_path: Optional[str] = None) -> bool:
    """
    Validate if the voter ID has already been used.
    """
    if not file_path:
        file_path = get_csv_path()

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == voter_id:
                    return False
    return True


def record_vote(voter_id: str, candidate: str, file_path: Optional[str] = None) -> None:
    """
    Record the vote in the CSV file.
    """
    if not file_path:
        file_path = get_csv_path()

    file_exists = os.path.exists(file_path)
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Voter ID', 'Candidate'])
        writer.writerow([voter_id, candidate])


def main() -> None:
    """
    Main function to manage the voting process via a command-line interface.
    """
    print("Welcome to the Voting System!")
    john_votes = 0
    jane_votes = 0

    ans = vote_menu()
    while ans == 'v':
        voter_id = input("Enter your Voter ID: ").strip()
        if not validate_voter(voter_id):
            print("Voter ID already used! You cannot vote again.")
        else:
            vote = candidate_menu()
            if vote == 1:
                john_votes += 1
                print("Voted John")
                record_vote(voter_id, "John")
            elif vote == 2:
                jane_votes += 1
                print("Voted Jane")
                record_vote(voter_id, "Jane")
        ans = vote_menu()
    print(f'John - {john_votes}, Jane - {jane_votes}, Total - {john_votes + jane_votes}')


if __name__ == "__main__":
    main()
