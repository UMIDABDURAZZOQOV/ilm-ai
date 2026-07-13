"""
Check if OpenSAT API includes images in questions
"""
import requests
import json

# Fetch a geometry question (likely to have images)
url = "https://pinesat.duckdns.org/api/questions"
params = {"section": "math", "domain": "Geometry and Trigonometry", "limit": 1}

print("Fetching geometry question from OpenSAT API...")
response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
questions = response.json()

if questions:
    q = questions[0]
    print("\n=== Question Structure ===")
    print(json.dumps(q, indent=2))
    
    print("\n=== Checking for image fields ===")
    print(f"Has 'image' field: {'image' in q}")
    print(f"Has 'image_url' field: {'image_url' in q}")
    print(f"Has 'diagram' field: {'diagram' in q}")
    print(f"Has 'figure' field: {'figure' in q}")
    
    # Check question object
    q_data = q.get("question", {})
    print(f"\nQuestion object keys: {list(q_data.keys())}")
    
    # Check if any field contains image data
    for key, value in q.items():
        if isinstance(value, str) and ("http" in value.lower() or "data:image" in value.lower()):
            print(f"\nFound potential image in field '{key}': {value[:100]}...")
else:
    print("No questions returned")
