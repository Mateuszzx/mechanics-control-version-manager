"""Status Manager for managing file statuses in a database.

This module provides functions for scanning, adding, and deleting files in the database.
"""

from pathlib import Path


def scan_and_add_new_files(conn, main_folder):
    """Scan the selected folder for files and add them to the database.

    Args:
        conn (sqlite3.Connection): The database connection.
        main_folder (str): Path to the folder to scan for files.

    This function scans the folder for files with specific extensions and adds
    them to the database if they are not already present.
    """
    allowed_ext = [".stl", ".step", ".sldprt", ".sldasm", ".stp"]
    cursor = conn.cursor()

    for file_path in Path(main_folder).rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in allowed_ext:
            relative_path = str(file_path.relative_to(main_folder))
            # Check if the file already exists in the database
            cursor.execute("SELECT id FROM files WHERE name = ?", (relative_path,))
            if cursor.fetchone() is None:
                # Insert the file into the database
                cursor.execute("""
                INSERT INTO files (name, version, status, notes, modified)
                VALUES (?, ?, ?, ?, ?)
                """, (relative_path, "v1.0", "in_progress", "", False))
    conn.commit()


def add_file_to_db(conn, filename):
    """Add a new file to the database.

    Args:
        conn (sqlite3.Connection): The database connection.
        filename (str): The name of the file to add.

    This function inserts a new file into the database with default metadata.
    """
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO files (name, version, status, notes, modified)
    VALUES (?, ?, ?, ?, ?)
    """, (filename, "v1.0", "in_progress", "", False))
    conn.commit()


def delete_files_from_db(conn, filenames):
    """Delete files from the database.

    Args:
        conn (sqlite3.Connection): The database connection.
        filenames (list): A list of filenames to delete.

    This function removes the specified files from the database.
    """
    cursor = conn.cursor()
    for filename in filenames:
        cursor.execute("DELETE FROM files WHERE name = ?", (filename,))
    conn.commit()
