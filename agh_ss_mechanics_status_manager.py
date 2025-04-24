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

    if data.get("files"):  # Jeśli są już pliki, nie robimy nic
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
        print(f"[~] Dodano {len(data['files'])} plików 3D do statusu.")
    else:
        print("[~] Nie znaleziono żadnych plików .stl/.step/etc.")

    save_status(data)

def add_file():
    filename = input("Nazwa pliku: ")
    version = input("Wersja (np. v1.0): ")
    status = input("Status (in_progress, under_review, final): ")
    notes = input("Notatki: ")
    data = load_status()
    data["files"].append({
        "name": filename,
        "version": version,
        "status": status,
        "modified": True,
        "notes": notes
    })
    save_status(data)
    print(f"[+] Dodano plik: {filename}")

def update_file():
    filename = input("Podaj nazwę pliku do aktualizacji: ")
    data = load_status()
    for f in data["files"]:
        if f["name"] == filename:
            version = input(f"Wersja ({f['version']}): ") or f["version"]
            status = input(f"Status ({f['status']}): ") or f["status"]
            notes = input(f"Notatki ({f['notes']}): ") or f["notes"]
            f["version"] = version
            f["status"] = status
            f["notes"] = notes
            f["modified"] = True
            save_status(data)
            print(f"[~] Zaktualizowano plik: {filename}")
            return
    print(f"[!] Nie znaleziono pliku: {filename}")


def show_last_commits(n=5):
    data = load_status()
    changelog = data.get("changelog", [])
    total = len(changelog)

    if not changelog:
        print("[~] Brak commitów do wyświetlenia.")
        return

    print(f"\nLast {min(n, total)} commits:\n")
    for commit in reversed(changelog[-n:]):
        print(f"🗓  {commit['date']} — {commit['author']}")
        for change in commit['changes']:
            print(f"   • {change}")
        print("-" * 30)


def add_commit():
    author = input("Autor: ")
    print("Wpisuj zmiany (pusta linia kończy):")
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
    print("[+] Commit dodany.")

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
        print(f"[+] Added {added_count} new 3D files.")  # on success
    else:
        print("[~] No new 3D files found.") 

def show_menu():
    print("\n===== MENU =====")
    print("1. Add new file")
    print("2. Update existing file")
    print("3. Add commit")
    print("4. Scan folder and add new 3D files")
    print("5. Show recent commits")
    print("6. Exit")
    print("================")


def main():
    initialize_files()

    while True:
        show_menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            add_file()
        elif choice == "2":
            update_file()
        elif choice == "3":
            add_commit()
        elif choice == "4":
            scan_and_add_new_files()
        elif choice == "5":
            try:
                n = int(input("How many recent commits to show? (default 5): ") or 5)
                show_last_commits(n)
            except ValueError:
                print("[!] Invalid number.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("[!] Invalid option.")



if __name__ == "__main__":
    main()
