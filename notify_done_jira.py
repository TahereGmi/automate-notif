import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Jira config
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Telegram config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Tracker file to avoid duplicate notifications
TRACKER_FILE = "notified_issues.txt"

headers = {
    "Authorization": f"Bearer {JIRA_API_TOKEN}",
    "Accept": "application/json"
}

def load_notified_issues():
    if not os.path.exists(TRACKER_FILE):
        return set()
    with open(TRACKER_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_notified_issue(issue_id):
    with open(TRACKER_FILE, "a") as f:
        f.write(issue_id + "\n")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)

def main():
    jql = f'project = {JIRA_PROJECT_KEY} AND status = Done AND updated >= -1d'
    url = f"{JIRA_BASE_URL}/rest/api/2/search?jql={jql}"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch issues:", response.status_code)
        print(response.text)
        return

    notified = load_notified_issues()
    issues = response.json().get("issues", [])

    for issue in issues:
        issue_id = issue["id"]
        if issue_id in notified:
            continue

        key = issue["key"]
        summary = issue["fields"]["summary"]
        issue_url = f"{JIRA_BASE_URL}/browse/{key}"
        message = f"✅ Jira Task Done:\n* {key} - {summary}\n{issue_url}"

        send_telegram_message(message)
        save_notified_issue(issue_id)

if __name__ == "__main__":
    main()
