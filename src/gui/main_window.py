""" Main window for the 3D File Version Tracker application."""

from tkinter import ttk
from pathlib import Path

from customtkinter import CTkFrame,CTkLabel, CTk

from src.gui.commit_display import CommitDisplay
from src.gui.buttons_panel import ButtonsPanel



class MainWindow(CTkFrame):
    """ Main window class for the 3D File Version Tracker application.
    This class handles the display of files, their statuses, and commit history.   
    """

    def __init__(self, parent, files_conn, commits_conn, author):
        super().__init__(parent)
        self.files_conn = files_conn
        self.commits_conn = commits_conn
        self.author = author

        # File Treeview
        self.tree = ttk.Treeview(self, columns=("version", "status", "notes", "author",
                                                        "last_modified_date"), show="tree")
        self.tree.heading("#0", text="File/Folder")
        for col in ("version", "status", "notes", "author", "last_modified_date"):
            self.tree.heading(col, text=col.replace("_", " ").title())

        self.tree.column("#0", width=300, anchor="w")
        self.tree.column("version", width=80, anchor="center")
        self.tree.column("status", width=160, anchor="center")
        self.tree.column("notes", width=260, anchor="w")
        self.tree.column("author", width=100, anchor="center")
        self.tree.column("last_modified_date", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Commit display
        self.commit_display = CommitDisplay(self, self.commits_conn)
        self.commit_display.pack(fill="x", padx=10, pady=5)

        # Latest commit info
        self.latest_commit_label = CTkLabel(self, text="", font=("Arial", 12))
        self.latest_commit_label.pack(pady=10)

        # Buttons panel
        self.buttons_panel = ButtonsPanel(self, self.files_conn, self.commits_conn, self.author,
                                        self.refresh_view, parent.main_folder)
        self.buttons_panel.pack(pady=5)

        self.refresh_view()

    def refresh_view(self):
        """Refresh the file tree and latest commit info."""
        print("DEBUG: Refreshing view...")  # Debugging

        # Clear the TreeView
        self.tree.delete(*self.tree.get_children())

        # Fetch files from the database
        cursor = self.files_conn.cursor()
        cursor.execute("SELECT name, version, status, notes, author, last_modified_date FROM files")
        files = cursor.fetchall()

        # Debugging: Print fetched files
        print("DEBUG: Fetched files:", files)

        # Populate the TreeView with the fetched files
        folder_nodes = {}
        for file in files:
            name, version, status, notes, author, last_modified_date = file
            filepath = Path(name)
            parent = ""

            # Handle folder hierarchy
            if filepath.parent != Path('.'):
                folder = str(filepath.parent)
                if folder not in folder_nodes:
                    folder_nodes[folder] = self.tree.insert("", "end", text=folder, open=True)
                parent = folder_nodes[folder]

            # Insert file into the TreeView
            self.tree.insert(parent, "end", text=filepath.name, values=(
                version, status, notes, author, last_modified_date
            ))

        # Fetch the latest commit info
        cursor = self.commits_conn.cursor()
        cursor.execute("SELECT date, author, changes FROM changelog ORDER BY id DESC LIMIT 1")
        latest_commit = cursor.fetchone()

        # Debugging: Print the latest commit
        print("DEBUG: Latest commit:", latest_commit)

        if latest_commit:
            date, author, changes = latest_commit
            self.latest_commit_label.configure(
                text=f"Last Commit: {changes} by {author} on {date}"
            )
        else:
            self.latest_commit_label.configure(text="No commits yet.")

        # Update the commit display
        self.commit_display.update_commits()


if __name__ == "__main__":
    app = CTk()
    main_window = MainWindow(app, None, None, "Author Name")
    main_window.pack(fill="both", expand=True)
    app.title("3D File Version Tracker")
    app.geometry("1000x600")
    app.mainloop()
