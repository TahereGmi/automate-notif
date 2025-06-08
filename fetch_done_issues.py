import requests
from dotenv import load_dotenv
import os

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")

# Use token in Authorization header
headers = {
    "Authorization": f"Bearer {JIRA_API_TOKEN}",
    "Accept": "application/json"
}

jql = f'project = {JIRA_PROJECT_KEY} AND status = Done AND updated >= -1d'
url = f"{JIRA_BASE_URL}/rest/api/2/search?jql={jql}"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    issues = response.json().get("issues", [])
    print(f"✅ Found {len(issues)} Done issue(s):\n")
    for issue in issues:
        key = issue['key']
        summary = issue['fields']['summary']
        print(f"- [{key}] {summary}")
else:
    print("❌ Error:", response.status_code)
    print(response.text)
