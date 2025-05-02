import sqlite3
from datetime import datetime
from src.utils.file_operations import scan_and_populate_files

def init_database(db_file, main_folder, author):
    """Initialize the SQLite database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        version TEXT NOT NULL,
        status TEXT NOT NULL,
        notes TEXT,
        modified BOOLEAN NOT NULL DEFAULT 0,
        author TEXT,
        last_modified_date TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS changelog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        author TEXT NOT NULL,
        changes TEXT NOT NULL
    )
    """)
    conn.commit()

    # Scan and populate files
    scan_and_populate_files(main_folder, conn)

    # Insert a changelog entry for initialization
    cursor.execute("""
    INSERT INTO changelog (date, author, changes)
    VALUES (?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), author,
        "Initialized database and scanned files"))
    conn.commit()

    return conn

def init_commits_database(db_file):
    """Initialize the SQLite database for commits."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the changelog table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS changelog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        author TEXT NOT NULL,
        changes TEXT NOT NULL
    )
    """)
    conn.commit()

    return conn
