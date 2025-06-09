import os
import datetime
from git_service import get_git_diff
from llm_service import generate_social_media_post

# --- Configuration ---
REPO_PATH = '.' # Path to your Git repository (current directory)
PLATFORMS = ["X", "Bluesky", "Mastodon"] # Social media platforms to generate posts for
DAY_COUNTER_FILE = 'day_counter.txt' # File to store the current day number

def get_current_day_number():
    """Reads the current day number from a file, increments it, and saves it back."""
    day_number = 1
    if os.path.exists(DAY_COUNTER_FILE):
        with open(DAY_COUNTER_FILE, 'r') as f:
            try:
                day_number = int(f.read().strip())
                day_number += 1 # Increment for the new day
            except ValueError:
                print(f"Warning: '{DAY_COUNTER_FILE}' contains invalid data. Starting day count from 1.")
                day_number = 1
    
    with open(DAY_COUNTER_FILE, 'w') as f:
        f.write(str(day_number))
    return day_number

def run_automation():
    """Orchestrates the process of getting diff, generating posts, and printing them."""
    print("--- Starting Social Media Post Automation ---")

    # 1. Get the current day number
    day_number = get_current_day_number()
    print(f"Current Day: {day_number}")

    # 2. Retrieve Git diff
    print("Retrieving Git diff for latest changes...")
    git_diff_content = get_git_diff(repo_path=REPO_PATH)

    if not git_diff_content:
        print("No significant Git changes detected or an error occurred while retrieving diff. No posts generated.")
        print("Please ensure you have new commits since the last run to generate a diff.")
        # Revert day number if no diff generated so it doesn't increment unnecessarily
        with open(DAY_COUNTER_FILE, 'w') as f:
            f.write(str(day_number - 1 if day_number > 1 else 1)) # Revert to previous day or keep at 1
        return

    print("Git diff successfully retrieved. Generating social media posts...")

    # 3. Generate posts for each platform
    generated_posts = {}
    for platform in PLATFORMS:
        print(f"\n--- Generating Post for {platform} ---")
        post = generate_social_media_post(git_diff_content, platform, day_number)
        generated_posts[platform] = post
        print(f"** {platform} Post **\n{post}")
        print("-" * 40) # Separator for readability

    print("\n--- Automation Finished ---")
    print("Generated Posts Summary:")
    for platform, post in generated_posts.items():
        print(f"  {platform}: {len(post.encode('utf-8'))} bytes (approx. {len(post)} chars)") # Using bytes for X char limit check approximation

if __name__ == "__main__":
    run_automation()