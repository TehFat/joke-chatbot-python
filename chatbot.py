import requests  # external library used to call the joke API over the internet
import json      # standard library module used to save/load conversation history
from datetime import datetime  # used to timestamp each message


class ChatBot:
    """Base chatbot: greets the user, replies to messages, and saves/loads history."""

    def __init__(self, name):
        # Runs automatically when a new ChatBot is created.
        self.name = name       # the bot's own name, e.g. "Jokey"
        self.history = []      # starts empty; filled in by load_history() or add_to_history()

    def greet(self):
        # Prints a simple opening message using the bot's name.
        print(f"Hello! My name is {self.name}. How can I assist you today?")

    # Function to load chat history from a JSON file
    def load_history(self):
        try:
            # Try to open the saved history file and load it back into self.history.
            with open("chat_history.json", "r") as file:
                self.history = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist yet (e.g. first time running the program),
            # just start with an empty history instead of crashing.
            self.history = []

    def save_history(self):
        # Writes the current self.history list to disk as JSON, so it can be
        # loaded again next time the program runs. indent=4 just makes the
        # saved file easier to read.
        with open("chat_history.json", "w") as file:
            json.dump(self.history, file, indent=4)

    def add_to_history(self, user_message, bot_reply):
        # Builds one record of a single exchange (timestamp + what was said)
        # and adds it to the in-memory history list. This does not save to
        # disk by itself — save_history() does that separately.
        entry = {
            "time": str(datetime.now()),
            "you": user_message,
            "bot": bot_reply
        }
        self.history.append(entry)

    # Function to fetch a random joke from an API
    def get_joke(self):
        try:
            # Send a request to the joke API and wait for its response.
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            if response.status_code == 200:
                # 200 means the request succeeded. Turn the response into a
                # Python dictionary and combine its two parts into one string.
                joke_data = response.json()
                return f"{joke_data['setup']} ... {joke_data['punchline']}"
            else:
                # The request went through, but the API didn't return success.
                return "Sorry, I couldn't fetch a joke at the moment."
        except requests.exceptions.ConnectionError:
            # No internet connection, or the API couldn't be reached at all.
            return "Sorry, I couldn't connect to the joke service. Please check your internet connection."
        except requests.exceptions.Timeout:
            # The API took too long to respond.
            return "Sorry, the request timed out. Please try again later."
        except requests.exceptions.RequestException as e:
            # Catches anything else that could go wrong with the request.
            # This is checked last because it's the most general case, and
            # Python stops at the first matching except block.
            return f"An error occurred: {e}"

    def respond(self, message):
        # Decides what to reply based on keywords in the user's message.
        # Conditions are checked in order, and only the first match runs.
        message = message.lower()  # normalize casing so "JOKE" and "joke" match the same way

        if "my name is" in message:
            # .split("my name is") cuts the message into pieces around that phrase,
            # e.g. "hi my name is fatima" -> ['hi ', ' fatima']. [-1] takes the last
            # piece, which is everything AFTER the phrase (the name itself).
            # .strip() then removes the leftover space at the start of that piece
            # (from "is fatima"), turning " fatima" into "fatima".
            name = message.split("my name is")[-1].strip()
            return f"Nice to meet you, {name.title()}! Want to hear a joke?"
        elif "i'm" in message or "i am" in message:
            # Same idea as above (split -> take the last piece -> strip extra spaces),
            # just applied to whichever of the two phrases ("i am" / "i'm") was
            # actually used, since people introduce themselves both ways.
            name = message.split("i am")[-1].strip() if "i am" in message else message.split("i'm")[-1].strip()
            return f"Nice to meet you, {name.title()}! Want to hear a joke?"
        elif "joke" in message:
            # Any message containing "joke" (that wasn't caught above) gets a joke.
            return self.get_joke()
        elif "hi" in message or "hello" in message:
            # Basic greeting.
            return f"Hey there! I'm {self.name}. Want to hear a joke?"
        else:
            # Fallback for anything that didn't match any condition above,
            # so the bot always replies with something instead of staying silent.
            return f"You said: '{message}'. I'm here to help!"


# Subclass that extends ChatBot to keep track of the number of jokes told
class SuperChatBot(ChatBot):
    """Adds joke-counting on top of everything ChatBot already does."""

    def __init__(self, name):
        # Reuse ChatBot's constructor (sets self.name and self.history),
        # then add one new attribute that only SuperChatBot has.
        super().__init__(name)
        self.joke_told = 0

    def get_joke(self):
        # Overrides ChatBot's get_joke(): reuse the original API-calling
        # logic via super(), then increase the counter before returning it.
        joke = super().get_joke()
        self.joke_told += 1
        return joke

    def joke_count(self):
        # New method — ChatBot doesn't have this at all.
        return f"I have told you {self.joke_told} joke(s) so far!"

    def respond(self, message):
        # Overrides ChatBot's respond(): check for the joke-count question
        # first, and hand everything else off to the original logic.
        message = message.lower()
        if "how many jokes" in message:
            return self.joke_count()
        else:
            return super().respond(message)


# --- Program starts here ---
bot = SuperChatBot("Jokey")   # create the chatbot
bot.load_history()           # bring back any previous conversation, if one exists
bot.greet()                  # print the opening message

# Main conversation loop: keeps running until the user types "exit" or "quit".
while True:
    message = input("You: ")
    if message.lower() in ["exit", "quit"]:
        bot.save_history()   # save the full conversation to disk before closing
        print("Goodbye! Have a great day!")
        break
    else:
        reply = bot.respond(message)         # decide what to reply
        print(f"{bot.name}: {reply}")        # show it to the user
        bot.add_to_history(message, reply)   # record this exchange in memory