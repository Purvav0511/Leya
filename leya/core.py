from git import Repo
from git.exc import GitCommandError

from .processors.repo_processor import process_repos
from .services.pincecone import embed_chunks_and_upload_to_pinecone, setup_pinecone_index, get_most_similar_chunks_for_query
from .utils.embedPrompt import build_prompt
from .utils.format_text import format_answer
from .services.openai import get_llm_answer
import os


def clone_repository(repo_url):
    try:
        # Determine the name of the repository by splitting the URL
        repo_name = repo_url.split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]

        # Path where the repository will be cloned
        leya_path = os.path.abspath(os.path.join(os.getcwd()))
        repos_path = os.path.join(leya_path, 'repos')
        repo_path = os.path.join(repos_path, repo_name)

        # Create the directory if it doesn't exist
        os.makedirs(repos_path, exist_ok=True)

        # Clone the repository
        print(f"Cloning repository {repo_url} into {repo_path}...")
        Repo.clone_from(repo_url, repo_path)
        print("Repository cloned successfully.")

        # Process Repos
        print("Processing Repos")
        code_chunks = process_repos(repo_name)
        print(code_chunks)
        print("Repos processed")

        # Setup Pinecone Index
        print("Setting up Pinecone Index...")
        index = setup_pinecone_index()

        if index:
            print("Index is present. Uploading to Pinecone...")
            # Uploading chunks to Pinecone
            print("Uploading code chunks to Pinecone...")
            print(index)
            embed_chunks_and_upload_to_pinecone(code_chunks, index, repo_name)
        else:
            print("Index does not exist. Skipping Pinecone upload.")

    except GitCommandError as e:
        print(f"An error occurred while cloning the repository: {e}")


def handle_query(query, repo_name, function_names):

    print(f"Handling query: {query} for repository: {repo_name}")
    context_chunks = get_most_similar_chunks_for_query(query, repo_name, function_names)
    prompt = build_prompt(query, context_chunks, repo_name)
    answer = get_llm_answer(prompt)
    formatted_answer = format_answer(answer)
    print("\n==== ANSWER ====\n")
    print(formatted_answer)
    print("\n==== ========== ======= ====== ===== ==== ====\n")


