""" Main window for the 3D File Version Tracker application."""

from tkinter import ttk, simpledialog, messagebox
from datetime import datetime

from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkToplevel, CTkComboBox, CTk

from src.utils.status_manager import scan_and_add_new_files
from src.gui.commit_display import CommitDisplay
from src.utils.file_actions import apply_status_to_files, commit_files, add_file_to_db, delete_files_from_db


class MainWindow(CTkFrame):
    """ Main window class for the 3D File Version Tracker application.
    This class handles the display of files, their statuses, and commit history.
    """

    def __init__(self, parent, conn, author):
        super().__init__(parent)
        self.conn = conn
        self.author = author  # Use the author passed from the App class

        # File Treeview
        columns = ("version", "status", "notes", "author", "last_modified_date")
        self.tree = ttk.Treeview(self, columns=columns, show="tree headings")
        self.tree.heading("#0", text="File/Folder")
        for col in columns:
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


        # Buttons
        btn_frame = CTkFrame(self)
        btn_frame.pack(pady=5)

        CTkButton(btn_frame, text="Commit Changes",
                command=self.commit_changes).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Change Status",
                command=self.change_status).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Scan for New Files",
                command=self.scan_files).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Add File",
                command=self.add_file).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Delete File",
                command=self.delete_file).pack(side="left", padx=5)


        self.refresh_view()

    def refresh_view(self):
        """Refresh the file tree and latest commit info."""
        self.tree.delete(*self.tree.get_children())
        cursor = self.conn.cursor()

        # Fetch files from the database
        cursor.execute("SELECT name, version, status, notes, author, last_modified_date FROM files")
        for row in cursor.fetchall():
            self.tree.insert("", "end", text=row[0], values=row[1:])

        # Fetch the latest commit info
        cursor.execute("SELECT date, author, changes FROM changelog ORDER BY id DESC LIMIT 1")
        latest_commit = cursor.fetchone()
        if latest_commit:
            date, author, changes = latest_commit
            self.latest_commit_label.configure(
                text=f"Last Commit: {changes} by {author} on {date}"
            )
        else:
            self.latest_commit_label.configure(text="No commits yet.")

        self.commit_display.update_commits()


    def change_status(self):
        """Change the status of the selected file(s) in the database."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select one or more files.")
            return

        # Define status options
        base_status_options = [
            "Author - is working on",
            "Final - Version",
            "Legacy",
            "Approved by...",
            "Rejected by..."
        ]

        # Create a customtkinter Toplevel window for selecting the new status
        status_window = CTkToplevel(self)
        status_window.title("Select New Status")
        status_window.geometry("400x200")
        status_window.resizable(False, False)

        # Add a label
        CTkLabel(status_window, text="Choose new status:", font=("Arial", 14)).pack(pady=10)

        # Add a dropdown menu (CTkComboBox)
        status_var = CTkComboBox(
            status_window,
            values=base_status_options,
            state="readonly",
            width=300
        )
        status_var.set(base_status_options[0])  # Set default value
        status_var.pack(pady=10)

        def apply_status():
            """Apply the selected status to the selected files."""
            selected_base = status_var.get()

            # Determine the new status based on the selected option
            if selected_base == "Approved by..." or selected_base == "Rejected by...":
                new_status = f"{selected_base.split()[0]} by {self.author}"
            elif selected_base == "Author - is working on":
                new_status = f"{self.author} is working on"
            else:
                new_status = selected_base

            filenames = [self.tree.item(item_id)["text"] for item_id in selected_items if self.tree.item(item_id)["values"]]
            updated_files = apply_status_to_files(self.conn, filenames, new_status, self.author)

            if updated_files:
                messagebox.showinfo("Success", f"Status updated for {len(updated_files)} file(s).")
            else:
                messagebox.showinfo("No Files Updated", "No files were matched or updated.")

            status_window.destroy()
            self.refresh_view()

        # Add an "Apply" button
        CTkButton(status_window, text="Apply", command=apply_status).pack(pady=20)

    def scan_files(self):
        """Scan for new files and add them to the database."""
        scan_and_add_new_files(self.conn, self.master.main_folder)
        self.refresh_view()
        messagebox.showinfo("Scan Complete", "New files (if any) have been added.")

    def add_file(self):
        """Add a new file to the database."""
        filename = simpledialog.askstring("File Name", "Enter the file name:")
        if not filename:
            return

        add_file_to_db(self.conn, filename)
        self.refresh_view()

    def delete_file(self):
        """Delete the selected file(s) from the database."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No selection", "Please select one or more files to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete",
"Are you sure you want to delete the selected file(s)?")
        if not confirm:
            return

        filenames = [self.tree.item(item_id)["text"] for item_id in selected_items
if self.tree.item(item_id)["values"]]
        delete_files_from_db(self.conn, filenames)
        self.refresh_view()

        if filenames:
            messagebox.showinfo("Success", f"Deleted {len(filenames)} file(s).")
        else:
            messagebox.showinfo("No files deleted", "No files were matched or deleted.")
            

    def commit_changes(self):
        """Commit the selected file(s) and add a changelog entry."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select one or more files.")
            return

        comment = simpledialog.askstring("Commit Comment", "Enter a comment for the commit:")
        if comment is None:
            return

        filenames = [self.tree.item(item_id)["text"] for item_id in selected_items if self.tree.item(item_id)["values"]]
        updated_files = commit_files(self.conn, filenames, comment, self.author)

        if updated_files:
            messagebox.showinfo("Success", f"{len(updated_files)} file(s) committed.")
        else:
            messagebox.showinfo("No Files Updated", "No files were matched or updated.")

        self.refresh_view()

if __name__ == "__main__":
    app = CTk()
    main_window = MainWindow(app, None, "Author Name")
    main_window.pack(fill="both", expand=True)
    app.title("3D File Version Tracker")
    app.geometry("1000x600")
    app.mainloop()
