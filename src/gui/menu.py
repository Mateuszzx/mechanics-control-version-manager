""" Custom menu for the 3D File Version Tracker application""" 
from customtkinter import CTkFrame, CTkButton


class AppMenu(CTkFrame):
    """Custom menu for the 3D File Version Tracker application."""

    def __init__(self, master, switch_project_callback, exit_callback, export_commits_callback):
        super().__init__(master, height=50)
        self.pack(fill="x", padx=10, pady=5)

        # Add buttons to the menu
        CTkButton(self, text="Switch Project Folder",
                        command=switch_project_callback).pack(side="left", padx=5)
        CTkButton(self, text="Export Commits (TXT)",
                        command=lambda: export_commits_callback("txt")).pack(side="left", padx=5)
        CTkButton(self, text="Export Commits (CSV)",
                        command=lambda: export_commits_callback("csv")).pack(side="left", padx=5)
        CTkButton(self, text="Export Commits (JSON)",
                        command=lambda: export_commits_callback("json")).pack(side="left", padx=5)
        CTkButton(self, text="Exit", command=exit_callback).pack(side="left", padx=5)
