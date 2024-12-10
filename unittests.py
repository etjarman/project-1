import unittest
from vote import validate_voter, record_vote, get_csv_path
import os

class TestVote(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a temporary test CSV file."""
        self.test_file = get_csv_path("test_data.csv")
        with open(self.test_file, "w") as file:
            file.write("Voter ID,Candidate\n")

    def tearDown(self) -> None:
        """Clean up the temporary test CSV file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_validate_voter(self) -> None:
        """Test voter ID validation."""
        record_vote("123", "John", self.test_file)
        self.assertFalse(validate_voter("123", self.test_file))  # ID exists
        self.assertTrue(validate_voter("456", self.test_file))   # ID does not exist

    def test_record_vote(self) -> None:
        """Test recording a vote."""
        record_vote("123", "John", self.test_file)
        with open(self.test_file, "r") as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 2)  # Header + 1 vote
        self.assertIn("123,John\n", lines)

if __name__ == "__main__":
    unittest.main()
