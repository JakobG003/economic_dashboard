import subprocess
import os

def get_git_diff(repo_path: str = '.', previous_commit: str = 'HEAD~1', current_commit: str = 'HEAD') -> str:
    """
    Retrieves the Git diff between two specified commits or between the last two commits.
    
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
        # Change the working directory to the repository path
        original_cwd = os.getcwd()
        os.chdir(repo_path)

        # Construct the Git diff command
        # --unified=0: Shows no context lines, focusing only on changed lines.
        # --diff-filter=d: Excludes deleted files from the diff (we're interested in added/modified).
        command = ['git', 'diff', f'{previous_commit}..{current_commit}', '--unified=0', '--diff-filter=d']
        
        # Execute the command, explicitly setting encoding to UTF-8 for Windows compatibility issues
        result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        
        # Return to the original directory
        os.chdir(original_cwd)

        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing Git command: {e}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")
        return ""
    except FileNotFoundError:
        print("❌ Git command not found. Please ensure Git is installed and in your system's PATH.")
        return ""
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return ""

# Example Usage (for independent testing of this module)
if __name__ == "__main__":
    # NOTE: This will only work if run inside a Git repository that has at least two commits.
    
    print("--- Retrieving diff for last commit vs. previous commit ---")
    latest_diff = get_git_diff() 
    
    if latest_diff:
        print("Successfully retrieved diff:")
        print(latest_diff) # This line is now uncommented to show the output
    else:
        print("Failed to retrieve diff. Please ensure you have at least two commits in your Git repository.")
        print("Tip: After making your first change and committing it, make another small change and commit that too.")
        print("Example Git commands for testing:")
        print("  git add .")
        print("  git commit -m \"Added a test change\"")
        print("  python git_service.py")