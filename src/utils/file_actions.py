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

def commit_files(conn, selected_files, comment, author):
    """Commit the selected files with a comment."""
    cursor = conn.cursor()
    updated_files = []

    for filename in selected_files:
        cursor.execute("SELECT version FROM files WHERE name = ?", (filename,))
        row = cursor.fetchone()
        if row:
            current_version = row[0]
            try:
                version_number = float(current_version.lstrip("v"))
                new_version = f"v{version_number + 0.01:.2f}"
            except ValueError:
                new_version = "v1.01"

            cursor.execute("""
            UPDATE files
            SET version = ?, notes = ?, modified = 1, author = ?, last_modified_date = ?
            WHERE name = ?
            """, (new_version, comment, author, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename))
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
            f"Committed {len(updated_files)} file(s): {', '.join(updated_files)} - {comment}"
        ))
        conn.commit()

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