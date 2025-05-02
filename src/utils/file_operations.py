""" File operations for the 3D file management system."""
from pathlib import Path
from datetime import datetime


def scan_and_populate_files(main_folder, conn):
    """Scan the selected folder for files and populate the database."""

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

def fetch_files(conn):
    """Fetch all files from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name, version, status, notes, author, last_modified_date FROM files")
    return cursor.fetchall()


def update_file_status(conn, filename, new_status, author):
    """Update the status, author, and last modified date of a file."""
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE files
    SET status = ?, author = ?, last_modified_date = ?, modified = 1
    WHERE name = ?
    """, (new_status, author, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename))
    conn.commit()


def update_file_notes(conn, filename, notes):
    """Update the notes for a file in the database."""
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE files
    SET notes = ?
    WHERE name = ?
    """, (notes, filename))
    conn.commit()


def add_changelog_entry(conn, author, changes):
    """Add a new entry to the changelog."""
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO changelog (date, author, changes)
    VALUES (?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), author, changes))
    conn.commit()


def fetch_latest_commit(conn):
    """Fetch the latest commit from the changelog."""
    cursor = conn.cursor()
    cursor.execute("SELECT date, author, changes FROM changelog ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()