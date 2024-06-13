import ast
import astunparse
import os

def chunk_code(file_path):
    with open(file_path, "r") as file:
        source = file.read()

    tree = ast.parse(source)

    chunks = []

    # Extract source file name
    file_name = os.path.basename(file_path)

    # Function to recursively traverse the AST and collect function and class definitions
    def traverse(node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Use astunparse to get the source code of the current node
            node_source = astunparse.unparse(node).strip()

            # Construct the definition string
            definition = node_source

            # Add the information to the list
            chunks.append({
                "function_name": node.name,
                "function_definition": definition,
                "source_file_name": file_name
            })

        for child_node in ast.iter_child_nodes(node):
            traverse(child_node)

    # Start recursive traversal from the root of the AST
    traverse(tree)

    return chunks



