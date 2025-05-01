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
    for path in Path(directory).rglob('*'):
        if path.is_file() and str(path) not in existing_files:
            new_files.append(str(path))
    return new_files