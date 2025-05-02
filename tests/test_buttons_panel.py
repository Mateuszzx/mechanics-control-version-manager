import unittest
from unittest.mock import MagicMock
from src.gui.buttons_panel import ButtonsPanel


class TestButtonsPanel(unittest.TestCase):
    def test_scan_files(self):
        mock_files_conn = MagicMock()
        mock_refresh_callback = MagicMock()
        panel = ButtonsPanel(None, mock_files_conn, None, "Author", mock_refresh_callback, "test_folder")

        panel.scan_files()
        mock_refresh_callback.assert_called_once()

    def test_add_file(self):
        mock_files_conn = MagicMock()
        mock_refresh_callback = MagicMock()
        panel = ButtonsPanel(None, mock_files_conn, None, "Author", mock_refresh_callback, "test_folder")

        with unittest.mock.patch("src.gui.buttons_panel.simpledialog.askstring", return_value="file1"):
            panel.add_file()
            mock_refresh_callback.assert_called_once()