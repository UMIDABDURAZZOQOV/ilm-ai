import os
from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("GEMINI_API_KEY", "")
print(f"Testing key starting with: {key[:5]}...")

client = genai.Client(api_key=key)

try:
    response = client.models.generate_content(
        model="gemini-1.5-flash", # Use a stable model for testing
        contents="Hi"
    )
    print("Success!")
    print(response.text)
except ClientError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
