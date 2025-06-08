import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import os

load_dotenv()

# Replace these with your real values or load from .env
JIRA_USERNAME = os.getenv("JIRA_USENAME")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

# Test endpoint (get current user info)
url = f"{JIRA_BASE_URL}/rest/api/2/myself"

auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_PASSWORD)
headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers, auth=auth)

print("Status code:", response.status_code)
print("Response:", response.text)
