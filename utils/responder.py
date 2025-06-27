import os
import requests
from dotenv import load_dotenv

# Load .env locally (ignored if not present or on Cloud Run)
load_dotenv()

# Try from env (Cloud Run) or .env (local)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY not found in environment variables or .env file.")

GROQ_MODELS_PRIORITY = [
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b",
    "gemma-7b-it"
]

def generate_answer(context, user_query):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    for model in GROQ_MODELS_PRIORITY:
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions using only the provided context."
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {user_query}"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 512
            }

            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=20
            )
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"].strip()

            print(f"[INFO] Response generated using model: {model}")
            return result

        except Exception as e:
            print(f"[WARN] Model {model} failed: {e}")
            continue

    return "❌ All Groq models failed to generate a response."
