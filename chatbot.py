import requests
import json
from datetime import datetime


class ChatBot:
    def __init__(self, name):
        self.name = name
        self.history = []

    def greet(self):
        print(f"Hello! My name is {self.name}. How can I assist you today?")

    # Function to load chat history from a JSON file
    def load_history(self):
        try:
            with open("chat_history.json", "r") as file:
                self.history = json.load(file)
        except FileNotFoundError:
            self.history = []

    def save_history(self):
        with open("chat_history.json", "w") as file:
            json.dump(self.history, file, indent=4)

    def add_to_history(self, user_message, bot_reply):
        entry = {
            "time": str(datetime.now()),
            "you": user_message,
            "bot": bot_reply
        }
        self.history.append(entry)

    # Function to fetch a random joke from an API
    def get_joke(self):
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            if response.status_code == 200:
                joke_data = response.json()
                return f"{joke_data['setup']} ... {joke_data['punchline']}"
            else:
                return "Sorry, I couldn't fetch a joke at the moment."
        except Exception as e:
            return f"An error occurred: {e}"

    def respond(self, message):
        message = message.lower()
        if "joke" in message:
            return self.get_joke()
        elif "hi" in message or "hello" in message:
            return f"Hey there! I'm {self.name}. Want to hear a joke?"
        else:
            return f"You said: '{message}'. I'm here to help!"


bot = ChatBot("Jokey")
bot.load_history()
bot.greet()

while True:
    message = input("You: ")
    if message.lower() in ["exit", "quit"]:
        bot.save_history()
        print("Goodbye! Have a great day!")
        break
    else:
        reply = bot.respond(message)
        print(f"{bot.name}: {reply}")
        bot.add_to_history(message, reply)