""" Utility functions for file actions in a database context.
This module provides functions to apply statuses, commit files, add new files """

from datetime import datetime

def apply_status_to_files(conn, selected_files, new_status, author):
    """Apply a new status to the selected files."""
    cursor = conn.cursor()
    updated_files = []

    for filename in selected_files:
        cursor.execute("""
        UPDATE files
        SET status = ?, author = ?, last_modified_date = ?, modified = 1
        WHERE name = ?
        """, (new_status, author, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename))
        updated_files.append(filename)

    conn.commit()

    if updated_files:
        # Add a changelog entry
        cursor.execute("""
        INSERT INTO changelog (date, author, changes)
        VALUES (?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            author,
            f"Changed status of {len(updated_files)} file(s) to '{new_status}'"
        ))
        conn.commit()

    return updated_files

def commit_files(files_conn, commits_conn, selected_files, comment, author):
    """Commit the selected files with a comment."""
    files_cursor = files_conn.cursor()
    commits_cursor = commits_conn.cursor()
    updated_files = []

    for filename in selected_files:
        files_cursor.execute("SELECT version FROM files WHERE name = ?", (filename,))
        row = files_cursor.fetchone()
        if row:
            current_version = row[0]
            try:
                version_number = float(current_version.lstrip("v"))
                new_version = f"v{version_number + 0.01:.2f}"
            except ValueError:
                new_version = "v1.01"

            print(f"DEBUG: Updating file {filename} to version {new_version}")  # Debugging
            files_cursor.execute("""
            UPDATE files
            SET version = ?, modified = 1, author = ?, last_modified_date = ?, notes = ?
            WHERE name = ?
            """, (new_version, author, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), comment, filename))
            updated_files.append(filename)

    files_conn.commit()

    if updated_files:
        print(f"DEBUG: Adding changelog entry for {updated_files}")  # Debugging
        commits_cursor.execute("""
        INSERT INTO changelog (date, author, changes)
        VALUES (?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            author,
            f"{comment} - Committed {len(updated_files)} file(s): {', '.join(updated_files)}"
        ))
        commits_conn.commit()

    return updated_files

def add_file_to_db(conn, filename):
    """Add a new file to the database."""
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO files (name, version, status, notes, modified)
    VALUES (?, ?, ?, ?, ?)
    """, (filename, "v1.0", "in_progress", "", False))
    conn.commit()

def delete_files_from_db(conn, filenames):
    """Delete files from the database."""
    cursor = conn.cursor()
    for filename in filenames:
        cursor.execute("DELETE FROM files WHERE name = ?", (filename,))
    conn.commit()

