import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GEMINI_API_KEY", "")

print(f"Testing key: {key[:10]}...")

# 1. Test as API Key (URL parameter)
url_api_key = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
payload = {"contents": [{"parts": [{"text": "Hi"}]}]}
print("\n--- Testing as Standard API Key (URL param) ---")
res1 = requests.post(url_api_key, json=payload)
print(f"Status: {res1.status_code}")
print(f"Response: {res1.text[:200]}")

# 2. Test as Bearer Token (Authorization Header)
url_bearer = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
print("\n--- Testing as Bearer Token (Authorization Header) ---")
res2 = requests.post(url_bearer, headers=headers, json=payload)
print(f"Status: {res2.status_code}")
print(f"Response: {res2.text[:200]}")
