import unittest
import parse

class TestSanitizer(unittest.TestCase):
    """Game log sanitizing test class."""

    def test_basic_cli(self):
        output = parse.main(["--help"])

if __name__ == '__main__':
    unittest.main()
