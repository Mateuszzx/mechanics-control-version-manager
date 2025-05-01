import yaml
from pathlib import Path

def load_status(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def save_status(data, filepath):
    with open(filepath, 'w') as file:
        yaml.dump(data, file)

def scan_and_add_new_files(directory, existing_files):
    new_files = []
    allowed_ext = [".stl", ".step", ".sldprt", ".sldasm", ".stp"]

    for path in Path(directory).rglob('*'):
        if path.is_file() and path.suffix.lower() in allowed_ext:  # Normalize to lowercase
            if str(path) not in existing_files:
                new_files.append(str(path))
    return new_files

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