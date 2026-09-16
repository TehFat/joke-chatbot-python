class ChatBot:
    def __init__ (self, name):
        self.name = name
        
    def greet(self):
        print(f"Hello! My name is {self.name}. How can I assist you today?")
 
    def respond(self, message):
        message = message.lower()
        if "joke" in message:
             return "Here's a joke: (coming soon — real jokes next!)"
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