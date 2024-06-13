import argparse
import os
from dotenv import load_dotenv
from .core import clone_repository, handle_query
from .repo_states import save_selected_repo, load_selected_repo
from .utils.set_enivronment_variables import set_environment_variables

def list_repositories(repos_path):
    """ Lists directories in the given path """
    try:
        repos = [repo for repo in os.listdir(repos_path) if os.path.isdir(os.path.join(repos_path, repo))]
        return repos
    except FileNotFoundError:
        return []
def main():
    load_dotenv()
    set_environment_variables()
    parser = argparse.ArgumentParser(description="Leya - Coding Assistant")
    parser.add_argument('-r', '--repo', type=str, help='Clone GitHub repository')
    parser.add_argument('-s', '--select', action='store_true', help='Select a repository to work with')
    parser.add_argument('-q', '--query', type=str, help='Query related to specific code issues')
    parser.add_argument('-f', '--functions', nargs='+', help='List of function names to focus the query on')

    args = parser.parse_args()

    if args.repo:
        clone_repository(args.repo)

    if args.select:
        repos_path = os.path.join(os.getcwd(), 'repos')
        repos = list_repositories(repos_path)
        if not repos:
            print("No repositories found. Please clone a repository first.")
            return

        print("Select a repository to query:")
        for idx, repo in enumerate(repos):
            print(f"{idx + 1}: {repo}")

        selection = input("Enter the number of the repository: ")
        try:
            selected_repo = repos[int(selection) - 1]
            selected_repo_path = os.path.join(repos_path, selected_repo)
            save_selected_repo(selected_repo_path)
            print(f"Repository selected: {selected_repo_path}")
        except (IndexError, ValueError):
            print("Invalid selection.")
            return
    if args.query:
        selected_repo_path = load_selected_repo()
        if not selected_repo_path:
            print("No repository selected. Please select a repository using the -s option.")
            return

        # Extract the repository name from the path
        selected_repo_name = os.path.basename(selected_repo_path)
        handle_query(args.query, selected_repo_name, args.functions)

if __name__ == "__main__":
    main()