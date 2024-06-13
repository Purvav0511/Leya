import os
import ast
from .file_processor import chunk_code
from ..utils.condense_file import read_and_condense_map
def parse_python_file(file_path):
    """Parse a Python file and return the formatted names of classes and functions."""
    with open(file_path, 'r', encoding='utf-8') as file:
        source = file.read()

    tree = ast.parse(source)
    definitions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            definitions.append(f"Function: {node.name}")
        elif isinstance(node, ast.ClassDef):
            definitions.append(f"Class: {node.name}")

    return definitions

def map_repo(directory, repo_name):
    repo_map = {}

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):  # Process Python files
                file_path = os.path.join(subdir, file)
                definitions = parse_python_file(file_path)
                # Find the index of the repo name in the path and slice from there
                repo_index = file_path.find(repo_name)
                if repo_index != -1:
                    relative_path = file_path[repo_index:]
                    repo_map[relative_path] = definitions

    return repo_map

def write_repo_map_to_file(repo_map, repo_name, file_path):
    """Write the repository map to a text file."""
    with open(file_path, 'w') as output_file:
        print(f"Processing repository: {repo_name}", file=output_file)
        for path, components in repo_map.items():
            print(f"{path}:", file=output_file)
            for component in components:
                print(f"  - {component}", file=output_file)



def process_repos(name):
    leya_path = os.path.abspath(os.path.join(os.getcwd()))  # Path to Leya directory
    repos_path = os.path.join(leya_path, 'repos')  # Path to repos directory inside Leya
    output_file_path = os.path.join(leya_path, 'repos', name, 'code-map.txt')  # Output file path in Leya/repos/<repo-name> directory
    chunks = []
    if os.path.exists(repos_path):
        repo_name = name
        repo_path = os.path.join(repos_path, repo_name)
        print(f"Processing repository: {repo_name}")

        if os.path.isdir(repo_path):
            repo_map = map_repo(repo_path, repo_name)  # Map the repository
            write_repo_map_to_file(repo_map, repo_name, output_file_path)  # Write initial verbose map to file

            # Read, condense, and overwrite the repository map
            condensed_map = read_and_condense_map(output_file_path)
            with open(output_file_path, 'w') as output_file:
                output_file.write(condensed_map)  # Overwrite with condensed map

            # Process code chunks for analysis

            for subdir, dirs, files in os.walk(repo_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(subdir, file)
                        file_chunks = chunk_code(file_path)  # Get chunks for the file
                        chunks.extend(file_chunks)

    return chunks



