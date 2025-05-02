import csv
import json
import os


def export_commits_to_txt(file_path, commits):
    """Export commits to a TXT file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Commit History\n")
        file.write("=" * 50 + "\n")
        for date, author, changes in commits:
            file.write(f"Date: {date}\n")
            file.write(f"Author: {author}\n")
            file.write(f"Changes: {changes}\n")
            file.write("-" * 50 + "\n")


def export_commits_to_csv(file_path, commits):
    """Export commits to a CSV file."""
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Author", "Changes"])
        writer.writerows(commits)


def export_commits_to_json(file_path, commits):
    """Export commits to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json_data = [{"date": date, "author": author, "changes": changes} for date, author, changes in commits]
        json.dump(json_data, file, indent=4)