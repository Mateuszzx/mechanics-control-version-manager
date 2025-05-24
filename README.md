# Control Version Manager

## Overview

The Control Version Manager is a Python application designed to track and manage versions of files in a 3D modeling environment. It provides a user-friendly interface to mark files as modified, change their status, and scan for new files, all while maintaining a changelog of recent commits.

## Features

- **File Version Tracking**: Easily manage and track versions of files.
- **Status Management**: Change the status of files with predefined options.
- **Commit History**: View recent commits and changes made to files.
- **User-Friendly Interface**: Built using CustomTkinter for a modern look and feel.

## Project Structure

``` Bash
control-version-manager
├── src
│   ├── app.py
│   ├── gui
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── file_tree_view.py
│   │   ├── commit_display.py
│   │   └── buttons_panel.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── file_operations.py
│   │   └── status_manager.py
├── requirements.txt
├── README.md
└── setup.py
```

## Installation

### For Normal Usage
1. Clone the repository:

   ``` Bash
   git clone <repository-url>
   ```

2. Unzip control-version-manager.zip file into directory on your computer.
3. Open folder, and create shortcut of app file (.exe extension).
4. Put shortcut on Desktop.

### Pure Python in Virtual Environment
1. Clone the repository:

   ``` Bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ``` Bash
   cd control-version-manager
   ```

3. Install the required dependencies:

   ``` Bash
   pip install -r requirements.txt
   ```

## Rules

1. **Do not delete or modify the .cvs folder or any files within it.**
These are essential for the version control system to function properly.

2. **Use a consistent username.**
This helps track contributions accurately across the project.

3. **Commit regularly.**
Ideally, make a commit after each work session to document progress clearly.

4. **Mark files before editing.
**If you're working on a file, check it out in the version control system first.

5. **Write clear and meaningful commit messages.**
Good commit messages make it easier to understand changes later.

6. **The system works best when these simple rules are followed.**
Consistency and discipline are key to effective collaboration.

## Dependencies

- CustomTkinter
- Other necessary libraries as specified in `requirements.txt`

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
