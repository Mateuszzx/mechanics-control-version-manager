""" Commit Display and Message Dialog """

from customtkinter import CTkFrame, CTkTextbox, CTkLabel, CTkToplevel, CTkEntry, CTkButton

class CommitDisplay(CTkFrame):
    """ Display recent commits in a text box.
    This class fetches the latest commits from the database
    and displays them in a scrollable text box.
    """

    def __init__(self, master, conn):
        super().__init__(master)
        self.conn = conn
        self.pack(fill="both", padx=10, pady=10, expand=True)

        self.commit_label = CTkLabel(self, text="Recent Commits:", font=("Arial", 32, "bold"))
        self.commit_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.commit_text = CTkTextbox(self, state="disabled",
                                    fg_color="#f5f5f5", text_color="#333")
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
                if " - " in changes:
                    message, changes = changes.split(": ", 1)
                else:
                    message, changes = changes, ""
                changes = changes.replace(", ", ",\n    *")
                self.commit_text.insert(
                    "end",
                    f"""Date: {date}
Author: {author}
Message: {message}
Changes:
    *{changes}

--------------------------------------------------
"""
                )

        self.commit_text.configure(state="disabled")


class CommitMessageDialog(CTkToplevel):
    """ Dialog for entering commit messages.
    This class creates a modal dialog that prompts the user
    """

    def __init__(self, master, title="Commit Message"):
        super().__init__(master)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        
        self.result = None  # Store the commit message result

        # Label for the prompt
        CTkLabel(self, text="Enter your commit message:", font=("Arial", 14)).pack(pady=10)

        # Entry widget for the commit message
        self.message_entry = CTkEntry(self, width=350)
        self.message_entry.pack(pady=10)

        # Buttons
        button_frame = CTkFrame(self)
        button_frame.pack(pady=10)

        CTkButton(button_frame, text="Submit", command=self.submit).pack(side="left", padx=5)
        CTkButton(button_frame, text="Cancel", command=self.cancel).pack(side="left", padx=5)

        # Grab focus and wait for the dialog to close
        self.grab_set()
        self.message_entry.focus()
        self.wait_window(self)

    def submit(self):
        """Handle the submit action."""
        self.result = self.message_entry.get().strip()
        self.destroy()

    def cancel(self):
        """Handle the cancel action."""
        self.result = None
        self.destroy()
