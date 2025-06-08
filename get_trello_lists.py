import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Replace these with your values
API_KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")

# Step 1: Get your Trello boards
boards_url = f"https://api.trello.com/1/members/me/boards?key={API_KEY}&token={TOKEN}"
boards_response = requests.get(boards_url)
boards = boards_response.json()

print("Your Trello Boards:\n")
for i, board in enumerate(boards):
    print(f"{i + 1}. {board['name']} (ID: {board['id']})")

# Step 2: Ask user to select a board
choice = int(input("\nEnter the number of the board you want to use: ")) - 1
selected_board_id = boards[choice]['id']

# Step 3: Get lists in the selected board
lists_url = f"https://api.trello.com/1/boards/{selected_board_id}/lists?key={API_KEY}&token={TOKEN}"
lists_response = requests.get(lists_url)
lists = lists_response.json()

print("\nLists in your selected board:\n")
for lst in lists:
    print(f"- {lst['name']} (ID: {lst['id']})")
