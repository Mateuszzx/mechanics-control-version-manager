from tkinter import Menu, filedialog, messagebox
from pathlib import Path
import sqlite3
import os

from customtkinter import CTk
from src.gui.main_window import MainWindow

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("3D File Version Tracker")
        self.geometry("1000x600")

        # Ask for the project folder at startup
        self.main_folder = self.ask_project_folder()
        if not self.main_folder:
            messagebox.showinfo("No Folder Selected", "No project folder selected. Exiting application.")
            self.destroy()
            return

        # Initialize the database
        self.db_file = self.main_folder / "project_data.db"
        self.conn = None
        self.init_database()
        self.update_title()

        # Create the menu bar
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        # Add "File" menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Switch Project Folder", command=self.switch_project_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Add the main window
        self.main_window = MainWindow(self, self.conn)
        self.main_window.pack(fill="both", expand=True)

    def ask_project_folder(self):
        """Ask the user to select a project folder at startup."""
        folder = filedialog.askdirectory(initialdir=Path.cwd(), title="Select Project Folder")
        return Path(folder) if folder else None

    def init_database(self):
        """Initialize the SQLite database."""
        self.conn = sqlite3.connect(self.db_file)
        cursor = self.conn.cursor()

        # Create tables if they don't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            modified BOOLEAN NOT NULL DEFAULT 0
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS changelog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            author TEXT NOT NULL,
            changes TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def switch_project_folder(self):
        """Open a dialog to select a new project folder."""
        new_folder = filedialog.askdirectory(initialdir=self.main_folder, title="Select Project Folder")
        if new_folder:
            self.main_folder = Path(new_folder)
            self.db_file = self.main_folder / "project_data.db"
            os.chdir(self.main_folder)  # Change the working directory
            self.init_database()  # Reinitialize the database
            self.update_title()
            self.main_window.refresh_view()  # Refresh the view to reflect the new folder

    def update_title(self):
        """Update the window title to include the current project folder."""
        self.title(f"3D File Version Tracker - {self.main_folder.name}")

if __name__ == "__main__":
    app = App()
    app.mainloop()