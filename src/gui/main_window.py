""" Main window for the 3D File Version Tracker application."""

from tkinter import ttk

from customtkinter import CTkFrame,CTkLabel, CTk

from src.gui.commit_display import CommitDisplay
from src.gui.buttons_panel import ButtonsPanel


class MainWindow(CTkFrame):
    """ Main window class for the 3D File Version Tracker application.
    This class handles the display of files, their statuses, and commit history.
    """

    def __init__(self, parent, conn, author):
        super().__init__(parent)
        self.conn = conn
        self.author = author  # Use the author passed from the App class

        # File Treeview
        self.tree = ttk.Treeview(self, columns=("version", "status", "notes", "author",
                                            "last_modified_date"), show="tree headings")

        self.tree.heading("#0", text="File/Folder")
        for col in ("version", "status", "notes", "author", "last_modified_date"):
            self.tree.heading(col, text=col.replace("_", " ").title())

        self.tree.column("#0", width=300, anchor="w")
        self.tree.column("version", width=80, anchor="center")
        self.tree.column("status", width=160, anchor="center")
        self.tree.column("notes", width=260, anchor="w")
        self.tree.column("author", width=100, anchor="center")
        self.tree.column("last_modified_date", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Commit display
        self.commit_display = CommitDisplay(self, self.conn)
        self.commit_display.pack(fill="x", padx=10, pady=5)

        # Latest commit info
        self.latest_commit_label = CTkLabel(self, text="", font=("Arial", 12))
        self.latest_commit_label.pack(pady=10)

        # Buttons panel
        self.buttons_panel = ButtonsPanel(self, conn, author, self.refresh_view, parent.main_folder)
        self.buttons_panel.pack(pady=5)

        self.refresh_view()

    def refresh_view(self):
        """Refresh the file tree and latest commit info."""
        self.tree.delete(*self.tree.get_children())
        cursor = self.conn.cursor()

        # Fetch files from the database
        cursor.execute("SELECT name, version, status, notes, author, last_modified_date FROM files")
        for row in cursor.fetchall():
            self.tree.insert("", "end", text=row[0], values=row[1:])

        self.commit_display.update_commits()


if __name__ == "__main__":
    app = CTk()
    main_window = MainWindow(app, None, "Author Name")
    main_window.pack(fill="both", expand=True)
    app.title("3D File Version Tracker")
    app.geometry("1000x600")
    app.mainloop()
