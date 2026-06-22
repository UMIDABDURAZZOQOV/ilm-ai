import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

models_to_try = ["gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash-8b", "gemini-2.0-flash"]

for m in models_to_try:
    try:
        print(f"Trying model: {m}")
        response = client.models.generate_content(
            model=m,
            contents="Hello, are you there?"
        )
        print(f"Success with {m}!")
        break
    except Exception as e:
        print(f"Failed with {m}: {e}")
