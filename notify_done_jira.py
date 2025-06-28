import os
from dotenv import load_dotenv
import time
import requests

load_dotenv()

# Jira config
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_FRONT_PROJECT_KEY = os.getenv("JIRA_FRONT_PROJECT_KEY")
JIRA_BACK_PROJECT_KEY = os.getenv("JIRA_BACK_PROJECT_KEY")
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

projects = [
    ("Frontend", JIRA_FRONT_PROJECT_KEY),
    ("Backend", JIRA_BACK_PROJECT_KEY)
]

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
    notified = load_notified_issues()

    # list of projects to scan
    projects = [
        ("Frontend", JIRA_FRONT_PROJECT_KEY),
        ("Backend", JIRA_BACK_PROJECT_KEY)
    ]

    for label, project_key in projects:
        jql = f'project = {project_key} AND status = Done AND updated >= -1d'
        url = f"{JIRA_BASE_URL}/rest/api/2/search?jql={jql}"
        
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch issues for {label} ({project_key}):", response.status_code)
            print(response.text)
            continue  # move on to next

        issues = response.json().get("issues", [])

        for issue in issues:
            issue_id = issue["id"]
            if issue_id in notified:
                continue  # already sent

            key = issue["key"]
            summary = issue["fields"]["summary"]
            issue_url = f"{JIRA_BASE_URL}/browse/{key}"

            # get the owner / assignee safely
            assignee_field = issue["fields"].get("assignee")
            if assignee_field is not None:
                assignee_name = assignee_field.get("displayName", "Unassigned")
            else:
                assignee_name = "Unassigned"

            message = (
                f"✅ {label} - [{assignee_name}]:\n"
                f"{summary}\n{issue_url}"
            )

            send_telegram_message(message)
            save_notified_issue(issue_id)
            time.sleep(1)

if __name__ == "__main__":
    main()
