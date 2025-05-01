from tkinter import ttk
from pathlib import Path
from customtkinter import CTkFrame
from src.utils.status_manager import load_status

class FileTreeView(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columns = ("version", "status", "notes", "assigned_by")
        self.tree = ttk.Treeview(self, columns=self.columns, show="tree headings")
        self.tree.heading("#0", text="File/Folder")
        for col in self.columns:
            self.tree.heading(col, text=col.replace("_", " ").title())

        self.tree.column("#0", width=300, anchor="w")
        self.tree.column("version", width=80, anchor="center")
        self.tree.column("status", width=160, anchor="center")
        self.tree.column("notes", width=260, anchor="w")
        self.tree.column("assigned_by", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
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