"""3D File Version Tracker Application"""

from pathlib import Path
from tkinter import filedialog
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkEntry, CTkToplevel
from src.gui.main_window import MainWindow
from src.utils.database_utils import init_database
from src.utils.workspace_utils import switch_workspace

class App(CTk):
    """Main application class for the 3D File Version Tracker."""

    def __init__(self):
        super().__init__()
        self.title("3D File Version Tracker")
        self.geometry("1200x800")

        # Ask for the project folder at startup
        self.main_folder = self.ask_project_folder()
        if not self.main_folder:
            self.show_info("No Folder Selected", "No project folder selected. Exiting application.")
            self.destroy()
            return

        # Ask for the author name
        self.author = self.ask_string("Your Name", "Enter your name (for commits and status updates):")
        if not self.author:
            self.author = "unknown"

        # Initialize the database
        self.db_file = Path(self.main_folder) / "project_data.db"
        if not self.db_file.exists():
            self.conn = init_database(self.db_file, self.main_folder, self.author)
        else:
            self.conn = switch_workspace(self.main_folder, self.db_file,
                                            self.author, self.show_info)
        # Create the custom menu
        self.create_menu()

        # Add the main window
        self.main_window = MainWindow(self, self.conn, self.author)
        self.main_window.pack(fill="both", expand=True)

    def create_menu(self):
        """Create a custom menu using CTkButton."""
        menu_frame = CTkFrame(self, height=50, fg_color="#f5f5f5")
        menu_frame.pack(fill="x", padx=10, pady=5)

        CTkButton(menu_frame, text="Switch Project Folder", command=self.switch_project_folder).pack(side="left", padx=5)
        CTkButton(menu_frame, text="Exit", command=self.quit).pack(side="left", padx=5)

    def show_info(self, title, message):
        """Display an info message using CTkToplevel."""
        info_window = CTkToplevel(self)
        info_window.title(title)
        info_window.geometry("300x150")
        CTkLabel(info_window, text=message, wraplength=280, font=("Arial", 12)).pack(pady=20)
        CTkButton(info_window, text="OK", command=info_window.destroy).pack(pady=10)

    def ask_string(self, title, prompt):
        """Display an input dialog using CTkToplevel."""
        input_window = CTkToplevel(self)
        input_window.title(title)
        input_window.geometry("300x150")

        CTkLabel(input_window, text=prompt, wraplength=280, font=("Arial", 12)).pack(pady=10)
        input_var = CTkEntry(input_window, width=250)
        input_var.pack(pady=10)

        def on_submit():
            self.input_value = input_var.get()
            input_window.destroy()

        CTkButton(input_window, text="Submit", command=on_submit).pack(pady=10)
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
            self.db_file = self.main_folder / "project_data.db"

            # Switch workspace
            self.conn = switch_workspace(self.main_folder, self.db_file, self.author, self.show_info)

            # Destroy the old MainWindow and create a new one
            self.main_window.destroy()
            self.main_window = MainWindow(self, self.conn, self.author)
            self.main_window.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
