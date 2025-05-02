import os
import sqlite3
from pathlib import Path
from src.utils.database_utils import init_database

def switch_workspace(main_folder, db_file, author, show_info_callback):
    """Switch the project workspace."""
    # Close the existing database connection
    conn = None
    if db_file.exists():
        conn = sqlite3.connect(db_file)

    # Change the working directory
    os.chdir(main_folder)

    # Reinitialize the database
    if not db_file.exists():
        show_info_callback("Database Not Found",
                    "Database file not found. A new one will be created.")
        conn = init_database(db_file, main_folder, author)
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM files")
        file_count = cursor.fetchone()[0]
        show_info_callback("Database Loaded", f"Loaded {file_count} files from the database.")

    return conn