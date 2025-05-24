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

1. Never delete/change .cvs folder and files inside.
2. Try always use the same username.
3. Create regular commits during work, the best way is one after each session.
4. If you work on some file, mark it in control version system before.
5. Write understandable commits.
6. Main strength of the system is following those simple rules.

## Dependencies

- CustomTkinter
- Other necessary libraries as specified in `requirements.txt`

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
