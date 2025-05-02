import unittest
from unittest.mock import patch, MagicMock
from src.utils.database_utils import init_database, init_commits_database


class TestDatabaseUtils(unittest.TestCase):
    @patch("src.utils.database_utils.sqlite3.connect")
    def test_init_database(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = init_database("test.db", "test_folder", "Test Author")
        self.assertEqual(conn, mock_conn)
        mock_conn.cursor().execute.assert_called()

    @patch("src.utils.database_utils.sqlite3.connect")
    def test_init_commits_database(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = init_commits_database("test_commits.db")
        self.assertEqual(conn, mock_conn)
        mock_conn.cursor().execute.assert_called()