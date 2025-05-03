"""Utility functions for exporting commit history to different formats.

This module provides functions to export commit history to TXT, CSV, and JSON formats.
"""

import csv
import json
import os
from tkinter import filedialog


def export_commits_to_txt(file_path, commits):
    """Export commits to a TXT file.

    Args:
        file_path (str): Path to the output TXT file.
        commits (list): List of commit records, each as a tuple (date, author, changes).
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Commit History\n")
        file.write("=" * 50 + "\n")
        for date, author, changes in commits:
            file.write(f"Date: {date}\n")
            file.write(f"Author: {author}\n")
            file.write(f"Changes: {changes}\n")
            file.write("-" * 50 + "\n")


def export_commits_to_csv(file_path, commits):
    """Export commits to a CSV file.

    Args:
        file_path (str): Path to the output CSV file.
        commits (list): List of commit records, each as a tuple (date, author, changes).
    """
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Author", "Changes"])
        writer.writerows(commits)


def export_commits_to_json(file_path, commits):
    """Export commits to a JSON file.

    Args:
        file_path (str): Path to the output JSON file.
        commits (list): List of commit records, each as a tuple (date, author, changes).
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json_data = [{"date": date, "author": author, "changes": changes}
                    for date, author, changes in commits]
        json.dump(json_data, file, indent=4)


def get_export_file_path(file_format):
    """Prompt the user to select a file path for export.

    Args:
        file_format (str): The format of the file to export (e.g., "txt", "csv", "json").

    Returns:
        str: The selected file path.
    """
    file_types = {
        "txt": [("Text Files", "*.txt"), ("All Files", "*.*")],
        "csv": [("CSV Files", "*.csv"), ("All Files", "*.*")],
        "json": [("JSON Files", "*.json"), ("All Files", "*.*")]
    }
    return filedialog.asksaveasfilename(
        title=f"Export Commits as {file_format.upper()}",
        defaultextension=f".{file_format}",
        filetypes=file_types.get(file_format, [("All Files", "*.*")])
    )


def export_commits(self, file_format):
    """Export commits to a file in the specified format."""
    cursor = self.commits_conn.cursor()
    cursor.execute("SELECT date, author, changes FROM changelog ORDER BY id ASC")
    commits = cursor.fetchall()

    if not commits:
        self.show_info("No Commits", "There are no commits to export.")
        return

    file_path = get_export_file_path(file_format)
    if not file_path:
        return

    # Export commits based on the selected format
    if file_format == "txt":
        export_commits_to_txt(file_path, commits)
    elif file_format == "csv":
        export_commits_to_csv(file_path, commits)
    elif file_format == "json":
        export_commits_to_json(file_path, commits)

    self.show_info("Export Successful",
                f"Commits have been exported to:\n{os.path.abspath(file_path)}")
