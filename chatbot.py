class ChatBot:
    def __init__ (self, name):
        self.name = name
        
    def greet(self):
        print(f"Hello! My name is {self.name}. How can I assist you today?")
 
bot = ChatBot("Jokey")           
bot.greet()

while True:
    message = input("You: ")
    if message.lower() in ["exit", "quit"]:
        print("Goodbye! Have a great day!")
        break
    else:
        print(f"{bot.name}: I'm here to help! You said: '{message}'")    