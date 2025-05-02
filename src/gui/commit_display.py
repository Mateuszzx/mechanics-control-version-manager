from customtkinter import CTkFrame, CTkTextbox, CTkLabel, CTkToplevel, CTkEntry, CTkButton

class CommitDisplay(CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master)
        self.conn = conn
        self.pack(fill="both", padx=10, pady=10, expand=True)

        self.commit_label = CTkLabel(self, text="Recent Commits:")
        self.commit_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.commit_text = CTkTextbox(self, height=300, state="disabled", fg_color="#f5f5f5", text_color="#333")
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

                # Split the commit message into the manually typed message and file-related changes
                if " - " in changes:  # Assuming "||" separates the manual message and file details
                    file_changes, manual_message = changes.split(" - ", 1)
                    manual_message = manual_message.strip()
                    file_changes = file_changes.strip()

                    # Format file-related changes if they contain multiple files
                    if "file(s):" in file_changes:
                        parts = file_changes.split(":")
                        if len(parts) > 1:
                            filenames = parts[1].strip().split(", ")
                            file_changes = "\n".join(f"* {filename}" for filename in filenames)
                else:
                    manual_message = changes
                    file_changes = ""

                # Display the commit details
                self.commit_text.insert(
                    "end",
                    f"""Date: {date}
Author: {author}
Message: {manual_message}
Changes:\n{file_changes}

#########################
"""
                )

        self.commit_text.configure(state="disabled")


class CommitMessageDialog(CTkToplevel):
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
