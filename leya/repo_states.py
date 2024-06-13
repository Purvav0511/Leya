# repo_state.py

import os

def save_selected_repo(repo_path):
    """Saves the selected repository's path to a file."""
    with open('.selected_repo', 'w') as file:
        file.write(repo_path)

def load_selected_repo():
    """Loads the selected repository's path from a file if it exists."""
    try:
        with open('.selected_repo', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def clear_selected_repo():
    """Clears the selected repository's path file if it exists."""
    if os.path.exists('.selected_repo'):
        os.remove('.selected_repo')
