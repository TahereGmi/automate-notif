import os
from dotenv import load_dotenv
import requests

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
response = requests.get(url)
print(response.json())
