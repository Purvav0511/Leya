
def condense_repo_map(repo_map):
    """
    Condense the repo map to minimize verbosity.
    """
    condensed_output = "Repository Content Summary:\n"
    for path, content in repo_map.items():
        classes = ', '.join(content['classes'])
        functions = ', '.join(content['functions'])
        condensed_output += f"{path}: Classes [{classes}], Functions [{functions}]\n"

    return condensed_output
def read_and_condense_map(file_path):
    """
    Read the repository map from a file and condense it for efficient processing.
    """
    repo_map = {}
    current_file = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.endswith(':'):
                # It's a file path
                current_file = line[:-1]  # Remove the colon
                repo_map[current_file] = {'classes': [], 'functions': []}
            elif line.startswith('- Class:'):
                # It's a class definition
                if current_file:
                    class_name = line.split(': ')[1]
                    repo_map[current_file]['classes'].append(class_name)
            elif line.startswith('- Function:'):
                # It's a function definition
                if current_file:
                    function_name = line.split(': ')[1]
                    repo_map[current_file]['functions'].append(function_name)

    return condense_repo_map(repo_map)