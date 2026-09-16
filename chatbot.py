import requests 
class ChatBot:
    def __init__ (self, name):
        self.name = name
        
    def greet(self):
        print(f"Hello! My name is {self.name}. How can I assist you today?")
    
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
bot.greet()

while True:
    message = input("You: ")
    if message.lower() in ["exit", "quit"]:
        print("Goodbye! Have a great day!")
        break
    else:
        reply = bot.respond(message)
        print(f"{bot.name}: {reply}")