"""Database Utilities for the 3D File Version Tracker.

This module provides functions for initializing and managing SQLite databases
for files and commits.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from src.utils.file_manager import scan_and_populate_files


def init_database(db_file, main_folder, author):
    """Initialize the SQLite database for files.

    Args:
        db_file (str): Path to the database file.
        main_folder (str): Path to the main folder to scan for files.
        author (str): Name of the author initializing the database.

    Returns:
        sqlite3.Connection: A connection to the initialized database.

    This function creates the necessary tables if they don't exist, scans the
    main folder for files, and populates the database with file metadata.
    """
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
    """Initialize the SQLite database for commits.

    Args:
        db_file (str): Path to the database file.

    Returns:
        sqlite3.Connection: A connection to the initialized database.

    This function creates the changelog table if it doesn't exist.
    """
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


def initialize_databases(main_folder, author):
    """Initialize the files and commits databases in a `.cvs` folder.

    Args:
        main_folder (str): Path to the main folder to scan for files.
        author (str): Name of the author initializing the databases.

    Returns:
        tuple: A tuple containing connections to the files and commits databases.

    This function ensures the `.cvs` folder exists, initializes both the files
    and commits databases, and returns their connections.
    """
    # Ensure the `.cvs` folder exists
    cvs_folder = Path(main_folder) / ".cvs"
    cvs_folder.mkdir(parents=True, exist_ok=True)  # Correctly create the folder

    # Define database file paths
    files_db_file = cvs_folder / "files_data.db"
    commits_db_file = cvs_folder / "commits_data.db"

    # Initialize the databases
    files_conn = init_database(files_db_file, main_folder, author)
    commits_conn = init_commits_database(commits_db_file)

    return files_conn, commits_conn
