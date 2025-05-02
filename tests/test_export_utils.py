import unittest
from unittest.mock import patch, mock_open
from src.utils.export_utils import export_commits_to_txt, export_commits_to_csv, export_commits_to_json


class TestExportUtils(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_export_commits_to_txt(self, mock_file):
        commits = [("2025-05-03", "Author", "Changes")]
        export_commits_to_txt("test.txt", commits)
        mock_file.assert_called_once_with("test.txt", "w", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    def test_export_commits_to_csv(self, mock_file):
        commits = [("2025-05-03", "Author", "Changes")]
        export_commits_to_csv("test.csv", commits)
        mock_file.assert_called_once_with("test.csv", "w", newline="", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    def test_export_commits_to_json(self, mock_file):
        commits = [("2025-05-03", "Author", "Changes")]
        export_commits_to_json("test.json", commits)
        mock_file.assert_called_once_with("test.json", "w", encoding="utf-8")