import subprocess
import os

def get_last_commit_diff(num_commits=1):
    """
    Gets the git diff output for the last N commits.

    Args:
        num_commits (int): The number of recent commits to get the diff for.
                            Default is 1 (the last commit).

    Returns:
        str: The git diff output as a string, or None if an error occurs.
    """
    try:
        # Check if we are in a git repository
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, capture_output=True)

        # Get the hash of the last commit
        last_commit_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], text=True
        ).strip()

        if num_commits == 1:
            # Get the diff between the last commit and its parent
            command = ['git', 'diff', 'HEAD~1', 'HEAD']
        else:
            # For multiple commits, get diff between HEAD and the commit N commits ago
            command = ['git', 'diff', f'HEAD~{num_commits}', 'HEAD']

        result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Git command not found. Please ensure Git is installed and in your PATH.")
        return None

def get_last_commit_message():
    """
    Gets the message of the last commit.

    Returns:
        str: The commit message as a string, or None if an error occurs.
    """
    try:
        # Check if we are in a git repository
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, capture_output=True)

        # Get the last commit message
        result = subprocess.run(['git', 'log', '-1', '--pretty=%B'], capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting last commit message: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Git command not found. Please ensure Git is installed and in your PATH.")
        return None


if __name__ == "__main__":
    # Simple test when run directly
    print("--- Testing get_last_commit_diff (last commit) ---")
    diff_output = get_last_commit_diff(num_commits=1)
    if diff_output:
        print(diff_output[:1000]) # Print first 1000 chars for brevity
    else:
        print("No diff or error occurred.")

    print("\n--- Testing get_last_commit_message ---")
    commit_message = get_last_commit_message()
    if commit_message:
        print(commit_message)
    else:
        print("No commit message or error occurred.")

    # Example of getting diff for last 2 commits
    print("\n--- Testing get_last_commit_diff (last 2 commits) ---")
    diff_output_2 = get_last_commit_diff(num_commits=2)
    if diff_output_2:
        print(diff_output_2[:1000])
    else:
        print("No diff for last 2 commits or error occurred.")