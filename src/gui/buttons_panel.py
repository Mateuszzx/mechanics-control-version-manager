from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkTextbox
from tkinter import messagebox, simpledialog

class ButtonsPanel(CTkFrame):
    def __init__(self, master, refresh_view_callback, mark_modified_callback, change_status_callback, scan_files_callback):
        super().__init__(master)

        self.refresh_view_callback = refresh_view_callback
        self.mark_modified_callback = mark_modified_callback
        self.change_status_callback = change_status_callback
        self.scan_files_callback = scan_files_callback

        self.create_widgets()

    def create_widgets(self):
        self.mark_modified_button = CTkButton(self, text="Mark as Modified", command=self.mark_modified)
        self.mark_modified_button.pack(side="left", padx=5)

        self.change_status_button = CTkButton(self, text="Change Status", command=self.change_status)
        self.change_status_button.pack(side="left", padx=5)

        self.scan_files_button = CTkButton(self, text="Scan for New Files", command=self.scan_files)
        self.scan_files_button.pack(side="left", padx=5)

        self.reload_yaml_button = CTkButton(self, text="Reload YAML", command=self.refresh_view)
        self.reload_yaml_button.pack(side="left", padx=5)

    def refresh_view(self):
        self.refresh_view_callback()

    def mark_modified(self):
        self.mark_modified_callback()

    def change_status(self):
        self.change_status_callback()

    def scan_files(self):
        self.scan_files_callback()