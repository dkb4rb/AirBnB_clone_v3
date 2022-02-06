"""Module test_console"""
import unittest
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class test_Console(unittest.TestCase):
    """Class to test the console"""
    @classmethod
    def setUpClass(self):
        """Sets a Class for testing"""
        self.console_1 = HBNBCommand()

    @classmethod
    def tearDownClass(self):
        """Test to delete the class created"""
        del self.console_1

    def test_do_create(self):
        """Testing do_create in the console"""
        with patch('sys.stdout', new=StringIO()) as mock:
            self.console_1.onecmd("create State numb=1")
            self.assertTrue(len(mock.getvalue()) >= 1)
        with patch('sys.stdout', new=StringIO()) as mock_2:
            self.console_1.onecmd("Show state" + mock.getvalue())
            self.assertTrue("numb" in mock_2.getvalue())

    def setup(self):
        """Reset FileStorage objects dictionary."""
        FileStorage._FileStorage__objects = {}
