import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise SystemExit("GROQ_API_KEY is not set in .env")

resp = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {api_key}"},
    timeout=15,
)

print("HTTP status:", resp.status_code)
print("\nModels available to your key:")
for model in resp.json().get("data", []):
    print(" -", model["id"])