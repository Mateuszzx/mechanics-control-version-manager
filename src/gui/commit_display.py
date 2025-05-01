from customtkinter import CTkFrame, CTkTextbox, CTkLabel

class CommitDisplay(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="x", padx=10, pady=5)

        self.commit_label = CTkLabel(self, text="Recent Commits:")
        self.commit_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.commit_text = CTkTextbox(self, height=10, state="disabled", fg_color="#f5f5f5")
        self.commit_text.pack(fill="x", padx=10, pady=5)

    def update_commits(self, commit_data):
        self.commit_text.configure(state="normal")
        self.commit_text.delete("1.0", "end")
        for commit in reversed(commit_data[-5:]):
            self.commit_text.insert("end", f"{commit['date']} — {commit['author']}\n")
            for change in commit["changes"]:
                self.commit_text.insert("end", f"  • {change}\n")
            self.commit_text.insert("end", "-" * 40 + "\n")
        self.commit_text.configure(state="disabled")