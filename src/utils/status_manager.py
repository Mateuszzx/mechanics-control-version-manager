import yaml
from datetime import datetime
from pathlib import Path
import os

def get_status_filename():
    current_folder = Path.cwd().name
    return f"{current_folder}_status.yaml"

STATUS_FILE = get_status_filename()

def load_status():
    if Path(STATUS_FILE).exists():
        with open(STATUS_FILE, "r") as f:
            return yaml.safe_load(f)
    else:
        return {
            "project": {
                "name": Path.cwd().name,
                "version": "v0.1",
                "description": "",
            },
            "status": {
                "last_updated": str(datetime.today().date()),
                "maintained_by": os.getenv("USER", "unknown"),
                "verified": False,
                "simulation_ready": False,
                "manufacture_ready": False,
            },
            "files": [],
            "changelog": []
        }

def save_status(data):
    data["status"]["last_updated"] = str(datetime.today().date())
    with open(STATUS_FILE, "w") as f:
        yaml.dump(data, f, sort_keys=False)

def initialize_files():
    status_path = Path(STATUS_FILE)
    needs_init = not status_path.exists()

    data = load_status()

    if data.get("files"):  # If files already exist, do nothing
        return

    print("[i] Initializing status — scanning 3D files...")

    allowed_ext = [".stl", ".step", ".sldprt", ".sldasm", ".stp"]
    base_path = Path.cwd()

    for file_path in base_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in allowed_ext:
            relative_path = str(file_path.relative_to(base_path))
            data["files"].append({
                "name": relative_path,
                "version": "v1.0",
                "status": "in_progress",
                "modified": False,
                "notes": ""
            })

    if data["files"]:
        print(f"[~] Added {len(data['files'])} 3D files to status.")
    else:
        print("[~] No .stl/.step/etc. files found.")

    save_status(data)

def add_file():
    filename = input("File name: ")
    version = input("Version (e.g., v1.0): ")
    status = input("Status (in_progress, under_review, final): ")
    notes = input("Notes: ")
    data = load_status()
    data["files"].append({
        "name": filename,
        "version": version,
        "status": status,
        "modified": True,
        "notes": notes
    })
    save_status(data)
    print(f"[+] Added file: {filename}")

def update_file():
    filename = input("Enter the file name to update: ")
    data = load_status()
    for f in data["files"]:
        if f["name"] == filename:
            version = input(f"Version ({f['version']}): ") or f["version"]
            status = input(f"Status ({f['status']}): ") or f["status"]
            notes = input(f"Notes ({f['notes']}): ") or f["notes"]
            f["version"] = version
            f["status"] = status
            f["notes"] = notes
            f["modified"] = True
            save_status(data)
            print(f"[~] Updated file: {filename}")
            return
    print(f"[!] File not found: {filename}")

def show_last_commits(n=5):
    data = load_status()
    changelog = data.get("changelog", [])
    total = len(changelog)

    if not changelog:
        print("[~] No commits to display.")
        return

    print(f"\nLast {min(n, total)} commits:\n")
    for commit in reversed(changelog[-n:]):
        print(f"🗓  {commit['date']} — {commit['author']}")
        for change in commit['changes']:
            print(f"   • {change}")
        print("-" * 30)

def add_commit():
    author = input("Author: ")
    print("Enter changes (empty line to finish):")
    changes = []
    while True:
        line = input("- ")
        if not line.strip():
            break
        changes.append(line)
    data = load_status()
    data["changelog"].append({
        "date": str(datetime.today().date()),
        "author": author,
        "changes": changes
    })
    save_status(data)
    print("[+] Commit added.")

def scan_and_add_new_files():
    data = load_status()
    existing_files = {f["name"] for f in data.get("files", [])}

    allowed_ext = [".stl", ".step", ".sldprt", ".sldasm", ".stp"]
    base_path = Path.cwd()
    added_count = 0

    for file_path in base_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in allowed_ext:
            relative_path = str(file_path.relative_to(base_path))
            if relative_path not in existing_files:
                data["files"].append({
                    "name": relative_path,
                    "version": "v1.0",
                    "status": "in_progress",
                    "modified": False,
                    "notes": ""
                })
                added_count += 1

    if added_count > 0:
        save_status(data)
        print(f"[+] Added {added_count} new 3D files.")
    else:
        print("[~] No new 3D files found.")

from datetime import datetime
from pathlib import Path

def update_file_status(data, filename, new_status, author):
    for f in data["files"]:
        if Path(f["name"]).as_posix() == filename:
            f["status"] = new_status
            f["modified"] = True
            f["assigned_by"] = author
            return True
    return False

def update_version_and_notes(data, filename, comment):
    for f in data["files"]:
        if Path(f["name"]).as_posix() == filename:
            try:
                v = float(f["version"].lstrip("v"))
                f["version"] = f"v{v + 0.01:.2f}"
            except Exception:
                f["version"] = "v1.01"
            f["notes"] = comment
            f["modified"] = True
            return True
    return False

def add_changelog_entry(data, author, changes):
    data["changelog"].append({
        "date": str(datetime.today().date()),
        "author": author,
        "changes": changes
    })