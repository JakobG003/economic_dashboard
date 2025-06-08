import os
from dotenv import load_dotenv # DODANO
import requests

print("Attempting to load .env file...")
dotenv_loaded = load_dotenv()

if dotenv_loaded:
    print("✅ .env file found and loaded successfully.")
else:
    print("❌ Warning: .env file not found or could not be loaded. Ensure it's in the project root.")

# Uporabimo ime spremenljivke iz .env datoteke
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_API_TOKEN:
    print("❌ Error: HF_API_TOKEN not found in environment variables (check .env file or system variables).")
else:
    print("✅ HF_API_TOKEN successfully read from environment.")
    if not HF_API_TOKEN.strip():
        print("❌ Error: HF_API_TOKEN is an empty string after trimming whitespace. Please check your .env file.")
    else:
        print(f"Token length (excluding leading/trailing spaces): {len(HF_API_TOKEN.strip())} characters.")
        print("Attempting to connect to Hugging Face Inference API...")

        # API URL za chat completions
        # Ta URL je bolj specifičen za chat modele in je odlična najdba!
        API_URL = "https://router.huggingface.co/hf-inference/models/HuggingFaceH4/zephyr-7b-beta/v1/chat/completions"
        
        # Glave za avtorizacijo - inicializiramo tukaj, ko je token že naložen
        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json" # Dodajanje content type je dobra praksa
        }

        def query(payload):
            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                response.raise_for_status() # Sproži izjemo za HTTP napake (4xx ali 5xx)
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"❌ HTTP/Request Error: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response body: {e.response.text}")
                return None
            except Exception as e:
                print(f"❌ General Error during API query: {e}")
                return None

        # Poskusni klic na model
        try:
            response = query({
                "messages": [
                    {
                        "role": "user",
                        "content": "What is the capital of France?"
                    }
                ],
                "model": "HuggingFaceH4/zephyr-7b-beta" # Model je tukaj pravilno naveden
                # Dodamo lahko tudi druge parametre, kot so max_tokens, temperature itd.
                # "max_tokens": 50,
                # "temperature": 0.7
            })

            if response and "choices" in response and response["choices"][0]["message"]["content"]:
                print("✅ Hugging Face response received successfully!")
                print("Zephyr 7B Beta response:", response["choices"][0]["message"]["content"].strip())
            else:
                print("❌ Hugging Face did not return a valid response.")
                print("Raw response object:", response)

        except Exception as e:
            print(f"❌ Error processing response or making API call: {e}")

print("\nTest finished.")