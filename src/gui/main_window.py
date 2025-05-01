from customtkinter import CTk, CTkFrame, CTkLabel, CTkTextbox, CTkButton
from tkinter import ttk, simpledialog, messagebox
from src.utils.status_manager import load_status, save_status, scan_and_add_new_files
from datetime import datetime
from pathlib import Path

class MainWindow(CTkFrame):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.conn = conn

        # Author input
        self.author = simpledialog.askstring("Your Name", "Enter your name (for commits and status updates):")
        if not self.author:
            self.author = "unknown"

        # File Treeview
        columns = ("version", "status", "notes", "assigned_by")
        self.tree = ttk.Treeview(self, columns=columns, show="tree headings")
        self.tree.heading("#0", text="File/Folder")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())

        self.tree.column("#0", width=300, anchor="w")
        self.tree.column("version", width=80, anchor="center")
        self.tree.column("status", width=160, anchor="center")
        self.tree.column("notes", width=260, anchor="w")
        self.tree.column("assigned_by", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Commit display
        self.commit_label = CTkLabel(self, text="Recent Commits:")
        self.commit_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.commit_text = CTkTextbox(self, height=10, state="disabled")
        self.commit_text.pack(fill="x", padx=10, pady=5)

        # Buttons
        btn_frame = CTkFrame(self)
        btn_frame.pack(pady=5)

        CTkButton(btn_frame, text="Mark as Modified", command=self.mark_modified).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Change Status", command=self.change_status).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Scan for New Files", command=self.scan_files).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Reload YAML", command=self.refresh_view).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Add File", command=self.add_file).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Refresh", command=self.refresh_view).pack(side="left", padx=5)

        self.refresh_view()

    def refresh_view(self):
        self.data = load_status()
        self.tree.delete(*self.tree.get_children())
        folder_nodes = {}

        for f in self.data.get("files", []):
            filepath = Path(f["name"])
            parent = ""

            if filepath.parent != Path('.'):
                folder = str(filepath.parent)
                if folder not in folder_nodes:
                    folder_nodes[folder] = self.tree.insert("", "end", text=folder, open=True)
                parent = folder_nodes[folder]

            self.tree.insert(parent, "end", text=filepath.name, values=(
                f["version"], f["status"], f.get("notes", ""), f.get("assigned_by", "")
            ))

        self.commit_text.configure(state="normal")
        self.commit_text.delete("1.0", "end")
        for commit in reversed(self.data.get("changelog", [])[-5:]):
            self.commit_text.insert("end", f"{commit['date']} — {commit['author']}\n")
            for change in commit["changes"]:
                self.commit_text.insert("end", f"  • {change}\n")
            self.commit_text.insert("end", "-" * 40 + "\n")
        self.commit_text.configure(state="disabled")

        cursor = self.conn.cursor()
        cursor.execute("SELECT name, version, status, notes FROM files")
        for row in cursor.fetchall():
            self.tree.insert("", "end", text=row[0], values=row[1:])

    def mark_modified(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No selection", "Please select one or more files.")
            return

        comment = simpledialog.askstring("Modification Comment", "Enter a shared comment for all selected files:")
        if comment is None:
            return

        def get_full_path(item_id):
            parts = []
            while item_id:
                parts.insert(0, self.tree.item(item_id)["text"])
                item_id = self.tree.parent(item_id)
            return Path("/".join(parts)).as_posix()

        updated_files = []
        for item_id in selected_items:
            if not self.tree.item(item_id)["values"]:
                continue  # skip folders

            filename = get_full_path(item_id)

            for f in self.data["files"]:
                if Path(f["name"]).as_posix() == filename:
                    try:
                        v = float(f["version"].lstrip("v"))
                        f["version"] = f"v{v + 0.01:.2f}"
                    except Exception:
                        f["version"] = "v1.01"
                    f["notes"] = comment
                    f["modified"] = True
                    f["assigned_by"] = self.author
                    updated_files.append(filename)
                    break

        if updated_files:
            self.data["changelog"].append({
                "date": str(datetime.today().date()),
                "author": self.author,
                "changes": [f"Marked '{name}' as modified with version bump and note." for name in updated_files]
            })
            save_status(self.data)
            self.refresh_view()
            messagebox.showinfo("Success", f"{len(updated_files)} file(s) marked as modified.")
        else:
            messagebox.showinfo("No files updated", "No files were matched or updated.")

    def change_status(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No selection", "Please select one or more files.")
            return

        base_status_options = [
            "Author - is working on",
            "Final - Version",
            "Legacy",
            "Approved by...",
            "Rejected by..."
        ]

        status_window = tk.Toplevel(self)
        status_window.title("Select New Status")
        status_window.geometry("350x180")

        tk.Label(status_window, text="Choose new status:").pack(pady=10)
        status_var = tk.StringVar(value=base_status_options[0])
        status_menu = ttk.Combobox(
            status_window, textvariable=status_var, values=base_status_options, state="readonly")
        status_menu.pack(pady=5)

        def get_full_path(item_id):
            parts = []
            while item_id:
                parts.insert(0, self.tree.item(item_id)["text"])
                item_id = self.tree.parent(item_id)
            return Path("/".join(parts)).as_posix()

        def apply_status():
            selected_base = status_var.get()

            if selected_base == "Approved by..." or selected_base == "Rejected by...":
                new_status = f"{selected_base.split()[0]} by {self.author}"
            elif selected_base == "Author - is working on":
                new_status = f"{self.author} is working on"
            else:
                new_status

            updated_files = []

            for item_id in selected_items:
                if not self.tree.item(item_id)["values"]:
                    continue  # Skip folders

                filename = get_full_path(item_id)

                for f in self.data["files"]:
                    if Path(f["name"]).as_posix() == filename:
                        f["status"] = new_status
                        f["modified"] = True
                        f["assigned_by"] = self.author
                        updated_files.append(filename)
                        break

            if updated_files:
                self.data["changelog"].append({
                    "date": str(datetime.today().date()),
                    "author": self.author,
                    "changes": [f"Changed status of '{name}' to '{new_status}'" for name in updated_files]
                })
                save_status(self.data)
                self.refresh_view()
                messagebox.showinfo("Success", f"{len(updated_files)} file(s) updated.")
            else:
                messagebox.showinfo("No files updated", "No files were matched or updated.")

            status_window.destroy()

        tk.Button(status_window, text="Apply", command=apply_status).pack(pady=10)

    def scan_files(self):
        scan_and_add_new_files()
        self.refresh_view()
        messagebox.showinfo("Scan complete", "New files (if any) have been added.")

    def add_file(self):
        """Add a new file to the database."""
        filename = simpledialog.askstring("File Name", "Enter the file name:")
        if not filename:
            return

        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO files (name, version, status, notes, modified)
        VALUES (?, ?, ?, ?, ?)
        """, (filename, "v1.0", "in_progress", "", False))
        self.conn.commit()
        self.refresh_view()

if __name__ == "__main__":
    app = CTk()
    main_window = MainWindow(app)
    main_window.pack(fill="both", expand=True)
    app.title("3D File Version Tracker")
    app.geometry("1000x600")
    app.mainloop()