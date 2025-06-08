import subprocess
import os

def get_git_diff(repo_path: str = '.', previous_commit: str = 'HEAD~1', current_commit: str = 'HEAD') -> str:
    """
    Retrieves the Git diff between two specified commits or the last two commits.

    Args:
        repo_path (str): The path to the Git repository. Defaults to the current directory.
        previous_commit (str): The identifier for the previous commit (e.g., 'HEAD~1', a commit hash).
                               Defaults to the commit before HEAD (the last commit).
        current_commit (str): The identifier for the current commit (e.g., 'HEAD', a commit hash).
                              Defaults to HEAD (the last commit).

    Returns:
        str: The Git diff output as a string, or an empty string if an error occurs.
    """
    try:
        # Change directory to the repository path
        original_cwd = os.getcwd()
        os.chdir(repo_path)

        # Construct the Git diff command
        # --unified=0 shows no context lines, focusing only on changed lines
        # --diff-filter=d excludes deleted files from the diff
        command = ['git', 'diff', f'{previous_commit}..{current_commit}', '--unified=0', '--diff-filter=d']
        
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Return to original directory
        os.chdir(original_cwd)

        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing Git command: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return ""
    except FileNotFoundError:
        print("❌ Git command not found. Please ensure Git is installed and in your system's PATH.")
        return ""
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return ""

# Example Usage (for testing this module independently)
if __name__ == "__main__":
    # IMPORTANT: This will only work if you run it inside a Git repository.
    # For testing, ensure your 'macro_dashboard' folder is a Git repository
    # (i.e., it has a .git folder in it).

    print("--- Getting diff for last commit vs. previous commit ---")
    # This assumes you have at least two commits in your repository
    latest_diff = get_git_diff() 
    if latest_diff:
        print("Successfully retrieved diff.")
        # print(latest_diff) # Uncomment to see the full diff output
    else:
        print("Failed to retrieve diff. Make sure you have at least two commits in your Git repository.")
        print("You can create a dummy commit like this: ")
        print("  git add .")
        print("  git commit -m \"Dummy commit for testing diff service\"")
        print("  # Then try running this script again.")

    print("\n--- Getting diff for a specific range (example) ---")
    # Replace 'commit_hash_1' and 'commit_hash_2' with actual hashes from your repo
    # specific_diff = get_git_diff(previous_commit='<commit_hash_1>', current_commit='<commit_hash_2>')
    # if specific_diff:
    #     print("Successfully retrieved specific diff.")
    # else:
    #     print("Failed to retrieve specific diff.")