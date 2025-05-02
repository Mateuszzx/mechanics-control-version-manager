import unittest
from unittest.mock import MagicMock
from src.utils.file_manager import fetch_files, commit_files


class TestFileManager(unittest.TestCase):
    def test_fetch_files(self):
        mock_conn = MagicMock()
        cursor = mock_conn.cursor.return_value
        cursor.fetchall.return_value = [("file1", "v1.0", "in_progress", "", "Author", "2025-05-03")]

        files = fetch_files(mock_conn)
        self.assertEqual(files, [("file1", "v1.0", "in_progress", "", "Author", "2025-05-03")])

    def test_commit_files(self):
        mock_files_conn = MagicMock()
        mock_commits_conn = MagicMock()
        cursor = mock_files_conn.cursor.return_value
        cursor.fetchone.return_value = ("v1.0",)

        updated_files = commit_files(mock_files_conn, mock_commits_conn, ["file1"], "Test Commit", "Author")
        self.assertEqual(updated_files, ["file1"])