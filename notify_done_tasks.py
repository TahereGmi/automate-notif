import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
DONE_LIST_ID = os.getenv("DONE_LIST_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Store already notified card IDs
NOTIFIED_CARDS_FILE = os.getenv("NOTIFIED_CARDS_FILE")

def get_done_cards():
    url = f"https://api.trello.com/1/lists/{DONE_LIST_ID}/cards?key={API_KEY}&token={TOKEN}"
    response = requests.get(url)
    return response.json()

def load_notified_cards():
    try:
        with open(NOTIFIED_CARDS_FILE, 'r') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def save_notified_card(card_id):
    with open(NOTIFIED_CARDS_FILE, 'a') as f:
        f.write(card_id + '\n')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text
    }
    requests.post(url, data=payload)

def main():
    cards = get_done_cards()
    notified_cards = load_notified_cards()

    for card in cards:
        if card['id'] not in notified_cards:
            message = f"✅ Task Completed:\n* {card['name']}\n{card['shortUrl']}"
            send_telegram_message(message)
            save_notified_card(card['id'])

if __name__ == '__main__':
    main()
