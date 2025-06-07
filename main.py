import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils.git_utils import get_last_commit_diff, get_last_commit_message

# Load environment variables from .env file
load_dotenv()

# --- Load API Keys ---
# X (Twitter) API Keys
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Mastodon API Keys and Info
MASTODON_BASE_URL = os.getenv("MASTODON_BASE_URL")
MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")

# Bluesky API Keys and Info
BLUESKY_USERNAME = os.getenv("BLUESKY_USERNAME")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")

# --- Verification (optional, for testing) ---
def verify_env_variables():
    """Verifies that all necessary environment variables are loaded."""
    required_vars = {
        "X": [X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET],
        "Gemini": [GEMINI_API_KEY],
        "Mastodon": [MASTODON_BASE_URL, MASTODON_ACCESS_TOKEN],
        "Bluesky": [BLUESKY_USERNAME, BLUESKY_PASSWORD]
    }

    all_present = True
    print("Verifying environment variables:")
    for platform, keys in required_vars.items():
        missing_keys_platform = []
        for key_value in keys:
            if not key_value:
                # Find the name of the missing key from os.getenv calls
                # This is a bit hacky, but works for verification purposes
                for var_name, value in globals().items():
                    if value is key_value and var_name.startswith(platform.upper()):
                        missing_keys_platform.append(var_name)
                        break
        if missing_keys_platform:
            print(f"  ❌ Missing API keys for {platform}: {', '.join(missing_keys_platform)}")
            all_present = False
        else:
            print(f"  ✅ All API keys for {platform} loaded successfully.")

    if all_present:
        print("\nAll necessary API keys loaded successfully. Ready to proceed!")
    else:
        print("\nSome API keys are missing. Please check your .env file.")
        # Optionally, exit the script if keys are critical
        # import sys
        # sys.exit(1)

def generate_summary_with_gemini(git_diff_content, commit_message):
    """
    Generates a concise summary of git changes using Google Gemini.

    Args:
        git_diff_content (str): The output of 'git diff'.
        commit_message (str): The message of the last commit.

    Returns:
        str: A summary of the changes, or None if generation fails.
    """
    if not GEMINI_API_KEY:
        print("Gemini API key is not set. Cannot generate summary.")
        return None

    model = genai.GenerativeModel('gemini-pro')
    prompt = (
        f"Review the following Git commit details:\n\n"
        f"Commit Message: {commit_message}\n\n"
        f"Git Diff:\n```diff\n{git_diff_content}\n```\n\n"
        f"Please generate a very concise (under 280 characters, suitable for a social media update) "
        f"and engaging summary of these changes. Focus on user-facing features or significant updates. "
        f"Start directly with the summary, without any introductory phrases like 'Here's a summary'."
    )

    try:
        response = model.generate_content(prompt)
        # Access text attribute directly
        summary = response.text.strip()

        # Optional: Truncate if it's still too long for Twitter/X (280 chars)
        if len(summary) > 280:
            summary = summary[:277] + "..." # Leave space for '...'
        return summary
    except Exception as e:
        print(f"Error generating content with Gemini: {e}")
        return None


if __name__ == "__main__":
    verify_env_variables()

    print("\n--- Testing Git Diff and Gemini Summary ---")
    diff = get_last_commit_diff()
    message = get_last_commit_message()

    if diff and message:
        print(f"Last Commit Message: {message}")
        print(f"Git Diff (first 500 chars): {diff[:500]}...") # Print a snippet
        gemini_summary = generate_summary_with_gemini(diff, message)
        if gemini_summary:
            print(f"\nGemini Generated Summary: {gemini_summary}")
            print(f"Summary Length: {len(gemini_summary)} characters")
        else:
            print("\nFailed to generate Gemini summary.")
    else:
        print("Could not retrieve Git diff or commit message. Is Git initialized and are there any commits?")

    print("\nmain.py executed.")
    # Tukaj bomo dodali logiko za objavljanje kasneje
