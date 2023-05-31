import unittest
import os
from tempfile import TemporaryDirectory

import app


# Add some simple unit tests just for the sake of the demo. Testing the app method would require more effort.

class TestFind(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.root_dir = self.temp_dir.name

        # Create a directory structure for testing
        os.makedirs(os.path.join(self.root_dir, "dir1"))
        os.makedirs(os.path.join(self.root_dir, "dir2"))

        # Create some files
        with open(os.path.join(self.root_dir, "file2.txt"), "w"):
            pass
        with open(os.path.join(self.root_dir, "file1.txt"), "w"):
            pass
        with open(os.path.join(self.root_dir, "file3.txt"), "w"):
            pass

    def tearDown(self):
        # Cleanup the tmp directory
        self.temp_dir.cleanup()

    def test_find_no_files(self):
        # Test when no files are found
        result = app.find("*.log", self.root_dir)
        self.assertEqual(result, [])

    def test_find_matching_files(self):
        # Test finding matching files
        result = app.find("*.txt", self.root_dir)
        expected = [
            os.path.join(self.root_dir, "file2.txt"),
            os.path.join(self.root_dir, "file1.txt"),
            os.path.join(self.root_dir, "file3.txt")
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
