import os
from dotenv import load_dotenv
import requests

# Model to be used for generating messages
LLM_MODEL = "HuggingFaceH4/zephyr-7b-beta"
# API URL for chat completions on the Hugging Face router
API_URL = f"https://router.huggingface.co/hf-inference/models/{LLM_MODEL}/v1/chat/completions"

def _get_hf_api_token():
    """
    Helper function to load the Hugging Face API token from environment variables.
    """
    if not os.getenv("HF_API_TOKEN"):
        load_dotenv()
    
    token = os.getenv("HF_API_TOKEN")
    if not token:
        raise ValueError("HF_API_TOKEN not found in environment variables. Please check your .env file.")
    return token

def generate_social_media_post(git_diff_content: str, platform: str, day_number: int) -> str:
    """
    Generates a concise and engaging social media post based on Git diff content,
    focusing on personal progress in building an economic dashboard from scratch with AI.

    Args:
        git_diff_content (str): The content of the Git diff describing dashboard changes.
        platform (str): The social media platform ('X', 'Bluesky', 'Mastodon').
        day_number (int): The current day number of the building process (e.g., 6).

    Returns:
        str: The generated social media post.
    """
    hf_api_token = _get_hf_api_token()
    headers = {
        "Authorization": f"Bearer {hf_api_token}",
        "Content-Type": "application/json"
    }

    # Updated system prompts with stronger constraints and specific instructions
    system_prompt_map = {
        "X": (
            "You are a developer sharing personal progress on building an economic dashboard from scratch with AI. "
            "Your goal is to create a short, impactful tweet (max 280 characters) for 'Day {day_num}' of this journey. "
            "Focus on *my* key learnings, challenges, or new features added. Use a personal, excited tone with relevant emojis and hashtags. "
            "Crucially, do NOT reference specific Git diff lines, file paths, line numbers, or any programming-specific jargon (e.g., 'SQLAlchemy', 'dataframe', 'Plotly', 'hovermode', specific functions like 'calculate_inflation'). "
            "Do NOT invent details or infer information not present in the diff (e.g., 'collaborated'). "
            "Describe *what* changed and *why* it matters for the dashboard's functionality or data, not *how* it was implemented. "
            "Ensure the post is a complete, coherent thought. Do not break off mid-sentence. "
            "Start with 'Day {day_num} of building my #EconomicDashboard with AI: '."
        ),
        "Bluesky": (
            "You are a developer sharing personal progress on building an economic dashboard from scratch with AI. "
            "Create a clear, engaging post for 'Day {day_num}' of this journey. Highlight *my* new insights, improvements, or features. "
            "Maintain a friendly, informative tone, use descriptive language, and relevant hashtags. "
            "Crucially, do NOT reference specific Git diff lines, file paths, line numbers, or any programming-specific jargon (e.g., 'SQLAlchemy', 'dataframe', 'Plotly', 'hovermode', specific functions). "
            "Do NOT invent details or infer information not present in the diff. "
            "Describe *what* changed and *why* it matters for the dashboard's functionality or data, not *how* it was implemented. "
            "Ensure the post is a complete, coherent thought. Do not break off mid-sentence. "
            "Start with 'Day {day_num} of my #EconomicDashboard journey (built with AI from scratch)! ✨ '."
        ),
        "Mastodon": (
            "You are a developer sharing personal progress on building an economic dashboard from scratch with AI. "
            "Craft a comprehensive, yet engaging, post for 'Day {day_num}' of this journey. "
            "Highlight significant changes, methodology improvements, or new data sources *I* implemented. "
            "Use a professional, insightful, and personal tone. Include relevant hashtags and consider adding more context if beneficial. "
            "Crucially, do NOT reference specific Git diff lines, file paths, line numbers, or any programming-specific jargon (e.g., 'SQLAlchemy', 'dataframe', 'Plotly', 'hovermode', specific functions). "
            "Do NOT invent details or infer information not present in the diff. "
            "Do NOT adopt the persona of an AI or say 'As an AI...' or similar. Always speak as 'I' the developer. "
            "Describe *what* changed and *why* it matters for the dashboard's functionality or data, not *how* it was implemented. "
            "Ensure the post is a complete and coherent narrative. Do not break off mid-sentence. "
            "Start with 'Day {day_num}: Building my #EconomicDashboard with AI from scratch. 📈 '."
        )
    }
    
    # Format the system prompt with the current day number
    system_prompt_template = system_prompt_map.get(platform, 
        "You are a helpful AI assistant tasked with summarizing data updates into engaging social media posts. "
        "Focus on key changes and add emojis and relevant hashtags."
    )
    system_prompt = system_prompt_template.format(day_num=day_number)

    # Main user message, kept general as the system prompt guides the persona
    user_message = (
        f"Here's a Git diff describing recent changes to the data dashboard. "
        f"Please summarize the key updates in a compelling post for {platform}. "
        f"Focus on *my* progress and what *I* built or learned today. "
        f"Use only the information provided in the diff:\n\n```diff\n{git_diff_content}\n```"
    )
    
    # Adjusted max_tokens to give more room for Bluesky/Mastodon to complete thoughts
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "model": LLM_MODEL,
        "max_tokens": 280 if platform == "X" else 400, # X has strict character limit, Bluesky/Mastodon more flexible
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()

        if response_json and "choices" in response_json and response_json["choices"][0]["message"]["content"]:
            return response_json["choices"][0]["message"]["content"].strip()
        else:
            print(f"❌ LLM did not return a valid response. Raw response: {response_json}")
            return "Error generating post."
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP/Request Error during LLM call: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return "Error communicating with LLM API."
    except Exception as e:
        print(f"❌ General Error during LLM call: {e}")
        return "An unexpected error occurred."

# Example Usage (for testing this module independently)
if __name__ == "__main__":
    # This is a test Git diff that you will replace with actual diffs later
    test_diff = """
diff --git a/dashboard.py b/dashboard.py
index a1b2c3d..e4f5g6h 100644
--- a/dashboard.py
+++ b/dashboard.py
@@ -10,6 +10,10 @@
 def load_data():
     # Old: load data from CSV
-    data = pd.read_csv('data.csv')
+    # New: switched to secure database connection
+    conn = create_db_connection()
+    data = pd.read_sql('SELECT * FROM economic_indicators', conn)
     return data
 
 def plot_trends():
@@ -25,3 +29,7 @@
     # Added new indicator: Inflation Rate
     df['inflation_rate'] = calculate_inflation(df['cpi'])
+    # Feature: Interactive tooltips for all charts
+    fig.update_layout(hovermode='x unified')
+    # Bug fix: Corrected unemployment rate calculation
+    df['unemployment'] = df['unemployment_raw'] * 100 
 """

    # You will need to manage the day number externally in your main program.
    # For testing, let's use a dummy day number.
    current_day = 6 

    print("--- Testing for X ---")
    x_post = generate_social_media_post(test_diff, "X", current_day)
    print(x_post)
    print("\n--- Testing for Bluesky ---")
    bluesky_post = generate_social_media_post(test_diff, "Bluesky", current_day)
    print(bluesky_post)
    print("\n--- Testing for Mastodon ---")
    mastodon_post = generate_social_media_post(test_diff, "Mastodon", current_day)
    print(mastodon_post)