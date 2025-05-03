"""Workspace Utilities for managing project workspaces.

This module provides functions for switching workspaces and reinitializing databases.
"""

import os
import sqlite3
from src.utils.database_utils import initialize_databases


def switch_workspace(main_folder, author, show_info_callback, parent):
    """Switch the project workspace.

    Args:
        main_folder (Path): Path to the new project folder.
        author (str): Name of the author switching the workspace.
        show_info_callback (function): Callback function to display informational messages.
        parent (CTk): The parent window for dialogs.

    Returns:
        tuple: A tuple containing connections to the files and commits databases.

    This function switches the workspace by connecting to existing databases
    or initializing new ones if they do not exist, and displays relevant messages.
    """
    # Ensure the main folder exists
    if not main_folder.exists():
        show_info_callback(parent, "Error", f"The folder '{main_folder}' does not exist.")
        return None, None

    # Change the working directory
    os.chdir(main_folder)

    # Define the `.cvs` folder and database file paths
    cvs_folder = main_folder / ".cvs"
    files_db_file = cvs_folder / "files_data.db"
    commits_db_file = cvs_folder / "commits_data.db"

    # Ensure the `.cvs` folder exists
    cvs_folder.mkdir(parents=True, exist_ok=True)

    # Check if the database files exist
    if files_db_file.exists() and commits_db_file.exists():
        # Connect to the existing databases
        files_conn = sqlite3.connect(files_db_file)
        commits_conn = sqlite3.connect(commits_db_file)
        show_info_callback(parent, "Workspace Loaded", f"Loaded existing workspace: {main_folder}")
    else:
        # Initialize new databases if they do not exist
        files_conn, commits_conn = initialize_databases(main_folder, author)
        show_info_callback(parent, "Workspace Initialized",
                            f"Initialized new workspace: {main_folder}")

    return files_conn, commits_conn
