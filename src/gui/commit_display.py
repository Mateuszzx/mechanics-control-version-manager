from customtkinter import CTkFrame, CTkTextbox, CTkLabel

class CommitDisplay(CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master)
        self.conn = conn
        self.pack(fill="both", padx=10, pady=10, expand=True)

        self.commit_label = CTkLabel(self, text="Recent Commits:")
        self.commit_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.commit_text = CTkTextbox(self, height=200, state="disabled", fg_color="#f5f5f5", text_color="#333")
        self.commit_text.pack(fill="both", padx=10, pady=10, expand=True)

    def update_commits(self):
        """Fetch and display recent commits from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT date, author, changes FROM changelog ORDER BY id DESC LIMIT 10")
        commits = cursor.fetchall()

        self.commit_text.configure(state="normal")
        self.commit_text.delete("1.0", "end")

        if not commits:
            self.commit_text.insert("end", "No commits found.\n")
        else:
            for commit in commits:
                date, author, changes = commit
                self.commit_text.insert("end", f"Date: {date}\nAuthor: {author}\nChanges: {changes}\n\n")

        self.commit_text.configure(state="disabled")