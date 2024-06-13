import os
PROMPT_LIMIT = 10000

def build_prompt(query, context_chunks, repo_name):
    # Initialize the prompt with the initial text
    prompt_start = "Answer the question based on the code snippets below. If the information is not sufficient, ask the users to provide more info.\n\n"

    # Load the repository map from the code-map.txt file
    repo_map_path = os.path.join(os.getcwd(), 'repos', repo_name, 'code-map.txt')
    with open(repo_map_path, 'r') as map_file:
        repo_map = map_file.read()

    # Add the repository map to the prompt
    prompt_repo_map = f"Code Structure:\n{repo_map}\n\n"


    # Add the query and answer sections
    prompt_end = f"\n\nQuestion: {query}\nAnswer:"

    # Start building the prompt with initial text
    prompt = prompt_start + prompt_repo_map

    # Iterate over each chunk and add it to the prompt if within the limit
    for chunk in context_chunks:
        chunk_text = f"\n\n---\n\nFunction: {chunk['function_name']} in {chunk['source_file_name']}\nCode:\n{chunk['function_definition']}\n"
        if len(prompt + chunk_text + prompt_end) > PROMPT_LIMIT:
            break
        prompt += chunk_text

    prompt += prompt_end
    return prompt