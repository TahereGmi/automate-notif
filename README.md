# Trello to Telegram Task Notifier

Trello-to-Telegram Task Notifier A simple Python automation that checks for completed tasks in a Trello board and automatically sends a notification to a private Telegram channel when tasks are moved to the "Done" list. The script runs twice a day and avoids duplicate messages.

## ✨ Features

- Connects to Trello using your API key and token
- Detects tasks in the "Done" list
- Sends a Telegram message for each new completed task
- Prevents duplicate notifications using a local tracker file
- Can be scheduled to run automatically (e.g. twice per day)

## 🔧 Setup

1. Get Trello API Key and Token from [trello.com/app-key](https://trello.com/app-key)
2. Create a Telegram bot using [@BotFather](https://t.me/botfather)
3. Add the bot to your private Telegram channel as an **admin**
4. Use `get_chat_id.py` to get your channel chat ID
5. Run `get_trello_lists.py` to find your board and Done list ID
6. Add your credentials in `notify_done_tasks.py`

## 🕐 Automation

To run this script on a schedule:

- Use `cron` (Linux/macOS) or Task Scheduler (Windows)
- Example: Run at 1 PM and 6 PM daily

## 🐍 Requirements

```bash
pip install requests
```
