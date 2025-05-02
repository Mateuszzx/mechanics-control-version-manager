from tkinter import simpledialog, messagebox

from customtkinter import CTkFrame, CTkButton, CTkToplevel, CTkComboBox, CTkLabel
from src.utils.file_actions import apply_status_to_files, commit_files, add_file_to_db, delete_files_from_db
from src.utils.status_manager import scan_and_add_new_files
from src.gui.commit_display import CommitMessageDialog  # Import the new dialog


class ButtonsPanel(CTkFrame):
    """Panel containing buttons for file operations."""
    
    def __init__(self, master, conn, author, refresh_callback, main_folder):
        super().__init__(master)
        self.conn = conn
        self.author = author
        self.refresh_callback = refresh_callback
        self.main_folder = main_folder

        # Buttons
        CTkButton(self, text="Commit Changes", command=
                            self.commit_changes).pack(side="left", padx=5)
        CTkButton(self, text="Change Status",
                            command=self.change_status).pack(side="left", padx=5)
        CTkButton(self, text="Scan for New Files",
                            command=self.scan_files).pack(side="left", padx=5)
        CTkButton(self, text="Add File",
                            command=self.add_file).pack(side="left", padx=5)
        CTkButton(self, text="Delete File",
                            command=self.delete_file).pack(side="left", padx=5)

    def commit_changes(self):
        """Commit the selected file(s) and add a changelog entry."""
        selected_items = self.master.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select one or more files.")
            return

        # Use the custom commit message dialog
        dialog = CommitMessageDialog(self)
        comment = dialog.result  # Get the result from the dialog
        if not comment:  # If the user cancels or submits an empty message
            return

        filenames = [self.master.tree.item(item_id)["text"] for item_id in selected_items if self.master.tree.item(item_id)["values"]]
        updated_files = commit_files(self.conn, filenames, comment, self.author)

        if updated_files:
            messagebox.showinfo("Success", f"{len(updated_files)} file(s) committed.")
        else:
            messagebox.showinfo("No Files Updated", "No files were matched or updated.")

        self.refresh_callback()

    def change_status(self):
        """Change the status of the selected file(s) in the database."""
        selected_items = self.master.tree.selection()
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

            filenames = [self.master.tree.item(item_id)["text"] for item_id in selected_items if self.master.tree.item(item_id)["values"]]
            updated_files = apply_status_to_files(self.conn, filenames, new_status, self.author)

            if updated_files:
                messagebox.showinfo("Success", f"Status updated for {len(updated_files)} file(s).")
            else:
                messagebox.showinfo("No Files Updated", "No files were matched or updated.")

            status_window.destroy()
            self.refresh_callback()

        # Add an "Apply" button
        CTkButton(status_window, text="Apply", command=apply_status).pack(pady=20)

    def scan_files(self):
        """Scan for new files and add them to the database."""
        scan_and_add_new_files(self.conn, self.main_folder)
        self.refresh_callback()
        messagebox.showinfo("Scan Complete", "New files (if any) have been added.")

    def add_file(self):
        """Add a new file to the database."""
        filename = simpledialog.askstring("File Name", "Enter the file name:")
        if not filename:
            return

        add_file_to_db(self.conn, filename)
        self.refresh_callback()

    def delete_file(self):
        """Delete the selected file(s) from the database."""
        selected_items = self.master.tree.selection()
        if not selected_items:
            messagebox.showinfo("No selection", "Please select one or more files to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected file(s)?")
        if not confirm:
            return

        filenames = [self.master.tree.item(item_id)["text"] for item_id in selected_items if self.master.tree.item(item_id)["values"]]
        delete_files_from_db(self.conn, filenames)
        self.refresh_callback()

        if filenames:
            messagebox.showinfo("Success", f"Deleted {len(filenames)} file(s).")
        else:
            messagebox.showinfo("No files deleted", "No files were matched or deleted.")