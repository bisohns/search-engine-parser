import os
import unittest
from unittest.mock import patch, MagicMock

from search_engine_parser.core import cli

engine_class_mock = MagicMock()
engine_class_mock.name = "Random Engine Name"
engine_class_mock.clear_cache = MagicMock()
engine_class_mock.search = MagicMock()

class CliTests(unittest.TestCase):

    def setUp(self):
        self.parser = cli.create_parser()

    def test_show_summary(self):
        args = self.parser.parse_args(["-e", "google", "--show-summary"])
        # If it executes properly it should return None
        self.assertTrue(cli.main(args) is None)

    @patch('search_engine_parser.core.cli.get_engine_class', return_value=engine_class_mock)
    def test_query(self, engine_class):
        args = self.parser.parse_args(["-e", "google", "--query", "Preach"])
        # If it executes properly it should return None
        self.assertTrue(cli.main(args) is None)
