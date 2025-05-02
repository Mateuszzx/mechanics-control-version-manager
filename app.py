"""3D File Version Tracker Application"""

import os
from pathlib import Path
from tkinter import filedialog

from customtkinter import CTk, CTkButton

from src.gui.main_window import MainWindow
from src.gui.menu import AppMenu
from src.utils.database_utils import init_database, init_commits_database
from src.utils.workspace_utils import switch_workspace
from src.utils.export_utils import export_commits_to_txt, export_commits_to_csv, export_commits_to_json
from src.utils.dialog_utils import create_info_dialog, create_input_dialog


class App(CTk):
    """Main application class for the 3D File Version Tracker."""

    def __init__(self):
        super().__init__()
        self.title("3D File Version Tracker")
        self.geometry("1400x800")

        self.main_folder = self.ask_project_folder()
        if not self.main_folder:
            self.show_info("No Folder Selected", "No project folder selected. Exiting application.")
            self.destroy()
            return

        # Ask for the author name
        self.author = self.ask_string("Your Name", "Enter your name (for commits updates):")
        if not self.author:
            self.author = "unknown"

        self.input_value = None

        # Initialize the databases
        self.files_db_file = Path(self.main_folder) / "files_data.db"
        self.commits_db_file = Path(self.main_folder) / "commits_data.db"

        self.files_conn = init_database(self.files_db_file, self.main_folder, self.author)
        self.commits_conn = init_commits_database(self.commits_db_file)

        # Create the custom menu
        self.menu = AppMenu(self, self.switch_project_folder, self.quit, self.export_commits)

        # Add the main window
        self.main_window = MainWindow(self, self.files_conn, self.commits_conn, self.author)
        self.main_window.pack(fill="both", expand=True)


    def show_info(self, title, message):
        """Display an info message."""
        info_window = create_info_dialog(self, title, message)
        info_window.grab_set()
        self.wait_window(info_window)

    def ask_string(self, title, prompt):
        """Display an input dialog."""
        input_window, input_var = create_input_dialog(self, title, prompt)

        def on_submit():
            self.input_value = input_var.get()
            input_window.destroy()

        submit_button = CTkButton(input_window, text="Submit", command=on_submit)
        submit_button.pack(pady=10)

        input_var.focus_set()
        input_window.bind("<Return>", lambda event: submit_button.invoke())

        input_window.grab_set()
        self.wait_window(input_window)
        return getattr(self, "input_value", None)

    def ask_project_folder(self):
        """Ask the user to select a project folder at startup."""
        return filedialog.askdirectory(title="Select Project Folder")

    def switch_project_folder(self):
        """Switch to a new project folder."""
        new_folder = self.ask_project_folder()
        if new_folder:
            self.main_folder = Path(new_folder)
            self.files_db_file = self.main_folder / "files_data.db"
            self.commits_db_file = self.main_folder / "commits_data.db"

            # Switch workspace
            self.files_conn = switch_workspace(self.main_folder, self.files_db_file,
                                                self.author, self.show_info)
            self.commits_conn = init_commits_database(self.commits_db_file)

            # Destroy the old MainWindow and create a new one
            self.main_window.destroy()
            self.main_window = MainWindow(self, self.files_conn, self.commits_conn, self.author)
            self.main_window.pack(fill="both", expand=True)

    def export_commits(self, file_format):
        """Export commits to a file in the specified format."""
        cursor = self.commits_conn.cursor()
        cursor.execute("SELECT date, author, changes FROM changelog ORDER BY id ASC")
        commits = cursor.fetchall()

        if not commits:
            self.show_info("No Commits", "There are no commits to export.")
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

        self.show_info("Export Successful",
            f"Commits have been exported to:\n{os.path.abspath(file_path)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
