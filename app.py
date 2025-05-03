"""3D File Version Tracker Application.

This module contains the main application class for managing 3D file versions,
including database initialization, GUI setup, and commit export functionality.
"""

import os
import sys
from pathlib import Path
from tkinter import filedialog

from customtkinter import CTk

from src.gui.main_window import MainWindow
from src.gui.menu import AppMenu
from src.utils.database_utils import init_database, init_commits_database
from src.utils.workspace_utils import switch_workspace
from src.utils.export_utils import (export_commits_to_txt, export_commits_to_csv,
                                    export_commits_to_json)
from src.utils.dialog_utils import show_info, ask_string


class App(CTk):
    """Main application class for the 3D File Version Tracker.

    This class initializes the application, manages the GUI, and handles
    interactions with the database and file system.
    """

    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.title("3D File Version Tracker")
        self.geometry("1400x800")
        self.iconbitmap(resource_path("src/assets/icon.ico"))

        self.main_folder = self.ask_project_folder()
        if not self.main_folder:
            show_info(self, "No Folder Selected",
                      "No project folder selected. Exiting application.")
            self.destroy()
            return

        # Ask for the author name
        self.author = ask_string(self, "Your Name", "Enter your name (for commits updates):")
        if not self.author:
            self.author = "unknown"

        # Initialize the databases in the `.cvs` folder
        self.files_conn, self.commits_conn = self.initialize_databases()

        # Create the custom menu
        self.menu = AppMenu(self, self.switch_project_folder, self.quit, self.export_commits)

        # Add the main window
        self.main_window = MainWindow(self, self.files_conn, self.commits_conn, self.author)
        self.main_window.pack(fill="both", expand=True)

    def ask_project_folder(self):
        """Ask the user to select a project folder at startup.

        Returns:
            str: The path to the selected project folder.
        """
        return filedialog.askdirectory(title="Select Project Folder")

    def initialize_databases(self):
        """Initialize the databases in the `.cvs` folder.

        Returns:
            tuple: A tuple containing connections to the files and commits databases.
        """
        cvs_folder = Path(self.main_folder) / ".cvs"
        cvs_folder.mkdir(parents=True, exist_ok=True)

        files_db_file = cvs_folder / "files_data.db"
        commits_db_file = cvs_folder / "commits_data.db"

        files_conn = init_database(files_db_file, self.main_folder, self.author)
        commits_conn = init_commits_database(commits_db_file)

        return files_conn, commits_conn

    def switch_project_folder(self):
        """Switch to a new project folder.

        This method updates the workspace, reinitializes the databases, and
        refreshes the main window.
        """
        new_folder = self.ask_project_folder()
        if new_folder:
            self.main_folder = Path(new_folder)

            # Use switch_workspace to handle workspace logic
            self.files_conn, self.commits_conn = switch_workspace(
                self.main_folder, self.author, show_info, self
            )

            if self.files_conn and self.commits_conn:
                # Destroy the old MainWindow and create a new one
                self.main_window.destroy()
                self.main_window = MainWindow(self, self.files_conn, self.commits_conn, self.author)
                self.main_window.pack(fill="both", expand=True)

    def export_commits(self, file_format):
        """Export commits to a file in the specified format.

        Args:
            file_format (str): The format to export the commits (e.g., "txt", "csv", "json").
        """
        cursor = self.commits_conn.cursor()
        cursor.execute("SELECT date, author, changes FROM changelog ORDER BY id ASC")
        commits = cursor.fetchall()

        if not commits:
            show_info(self, "No Commits", "There are no commits to export.")
            return

        # Ask the user where to save the file
        file_extension = file_format.lower()
        file_types = {
            "txt": [("Text Files", "*.txt"), ("All Files", "*.*")],
            "csv": [("CSV Files", "*.csv"), ("All Files", "*.*")],
            "json": [("JSON Files", "*.json"), ("All Files", "*.*")]
        }
        file_path = filedialog.asksaveasfilename(
            title=f"Export Commits as {file_format.upper()}",
            defaultextension=f".{file_extension}",
            filetypes=file_types.get(file_format, [("All Files", "*.*")])
        )
        if not file_path:
            return

        # Export commits based on the selected format
        if file_format == "txt":
            export_commits_to_txt(file_path, commits)
        elif file_format == "csv":
            export_commits_to_csv(file_path, commits)
        elif file_format == "json":
            export_commits_to_json(file_path, commits)

        show_info(self, "Export Successful",
                f"Commits have been exported to:\n{os.path.abspath(file_path)}")



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = App()
    app.mainloop()
