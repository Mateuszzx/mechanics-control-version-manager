"""3D File Version Tracker Application"""

from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkEntry, CTkToplevel
from pathlib import Path
import sqlite3
import os
from datetime import datetime

from src.gui.main_window import MainWindow
from src.utils.file_operations import scan_and_populate_files

class App(CTk):
    """Main application class for the 3D File Version Tracker."""

    def __init__(self):
        super().__init__()
        self.title("3D File Version Tracker")
        self.geometry("1200x800")

        # Ask for the project folder at startup
        self.main_folder = self.ask_project_folder()
        self.title("3D File Version Tracker")
        self.geometry("1200x800")

        # Ask for the project folder at startup
        self.main_folder = self.ask_project_folder()
        if not self.main_folder:
            messagebox.showinfo("No Folder Selected",
                                "No project folder selected. Exiting application.")
            self.destroy()
            return

        # Ask for the author name
        self.author = simpledialog.askstring("Your Name",
                                "Enter your name (for commits and status updates):")
        if not self.author:
            self.author = "unknown"

        # Initialize the database
        self.db_file = self.main_folder / "project_data.db"
        self.conn = None
        if not self.db_file.exists():
            messagebox.showinfo("Database Not Found",
                                "Database file not found. A new one will be created.")
            self.init_database()
        else:
            self.conn = sqlite3.connect(self.db_file)
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM files")
            file_count = cursor.fetchone()[0]
            if file_count == 0:
                messagebox.showinfo("No Files Found",
                            "No files found in the database. Please scan the project folder.")
                self.init_database()
            else:
                messagebox.showinfo("Database Loaded",
                                    f"Loaded {file_count} files from the database.")
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
        self.main_window = MainWindow(self, self.conn, self.author)
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
            modified BOOLEAN NOT NULL DEFAULT 0,
            author TEXT,
            last_modified_date TEXT
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

        # Scan and populate files
        scan_and_populate_files(self.main_folder, self.conn)

        # Insert a changelog entry for initialization
        cursor.execute("""
        INSERT INTO changelog (date, author, changes)
        VALUES (?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.author,
                            "Initialized database and scanned files"))
        self.conn.commit()

    def switch_project_folder(self):
        """Open a dialog to select a new project folder."""
        new_folder = filedialog.askdirectory(initialdir=self.main_folder, title="Select Project Folder")
        if new_folder:
            self.main_folder = Path(new_folder)
            self.db_file = self.main_folder / "project_data.db"

            # Close the existing database connection
            if self.conn:
                self.conn.close()

            # Change the working directory
            os.chdir(self.main_folder)

            # Reinitialize the database
            if not self.db_file.exists():
                messagebox.showinfo("Database Not Found", "Database file not found. A new one will be created.")
                self.init_database()
            else:
                self.conn = sqlite3.connect(self.db_file)
                cursor = self.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM files")
                file_count = cursor.fetchone()[0]
                messagebox.showinfo("Database Loaded", f"Loaded {file_count} files from the database.")

            # Update the title
            self.update_title()

            # Destroy the old MainWindow and create a new one
            self.main_window.destroy()
            self.main_window = MainWindow(self, self.conn, self.author)
            self.main_window.pack(fill="both", expand=True)

    def update_title(self):
        """Update the window title to include the current project folder."""
        self.title(f"3D File Version Tracker - {self.main_folder.name}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
