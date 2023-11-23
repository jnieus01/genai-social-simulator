import redis
import json
import random
import os 

class Chatbot:
    def __init__(self, username, host='redis', port=6379):
        self.client = redis.StrictRedis(host=host, port=port)
        self.pubsub = self.client.pubsub()
        self.username = username
        self.commands = {
            "identify":    self.identify_user,
            "join":    self.join_channel,
            "leave":    self.leave_channel,
            "send":    self.send_message,
            "listen":    self.listen_to_messages,
            "dm":    self.direct_message,
            "list channels":    self.list_channels,
            "weather":    self.weather,
            "fact":    self.show_fact,
            "whoami":    self.show_user_info,
            "!help":    self.show_help,
            "quit":    self.quit_chat
        }
        self.intro_message = "Hi! I am a chatbot. You can call me Cathy.\n[Options]\n"
        self.opts_message = "\n".join([f"{cmd}: {func.__doc__}" for cmd, func in self.commands.items()])

    def prompt_input(self, *questions):
        return [input(q) for q in questions]

    def get_docstring(self, command):
        function = self.commands.get(command)
        # print the docstring for a function if it exists
        if function:
            print(function.__doc__)
        else:
            print(f"No documentation found for {command}")

    def identify_user(self):
        """Enter your info."""
        name, age, sex, location = self.prompt_input("Enter your name: ", "Enter your age: ", "Enter your sex: ", "Enter your location: ")
        user_key = f"user:{name}"
        self.client.hset(user_key, mapping={"name": name, "age": age, "sex": sex, "location": location})
        self.username = name
        print("\nUser info was saved successfully!")

    def join_channel(self):
        """Subscribe to a Redis channel"""
        channels_input = input("Please provide the channel(s) you'd like to subscribe to (separated by commas): ").strip()
        print("\n")
        channels_to_subscribe = [channel.strip() for channel in channels_input.split(",")]

        channels_key = f"channels:{self.username}"

        for channel in channels_to_subscribe:
            # Update channels record
            self.client.sadd(channels_key, channel)
            # Subscribe user to the channel
            self.pubsub.subscribe(channel)
            print(f"Subscribed to {channel}")

        # Print message to show channel membership
        your_channels = self.client.smembers(channels_key)
        print(f"\nYour channels: {', '.join(map(lambda x: x.decode('utf-8'), your_channels))}")

    def leave_channel(self):
        """Leave a channel"""
        channel = input("\nWhich channel would you like to leave? ")
        channels_key = f"channels:{self.username}"
        self.client.srem(channels_key, channel)
        self.pubsub.unsubscribe(channel)
        print(f"\nUnsubscribed from [{channel}]")

    def send_message(self):
        """Send a message to a channel"""
        channel = input("\nWhich channel would like to message? ")
        message = input("\nInput message here: ") 
        message_obj = {
            "from": self.username,
            "message": message
        }
        self.client.publish(channel, json.dumps(message_obj)) 

    def listen_to_messages(self):
        """Listen to a channel"""
        channels_input = input("\nProvide channels to listen to (separated by commas): ").strip()
        channels_to_listen = [channel.strip() for channel in channels_input.split(",")]

        self.pubsub.subscribe(*channels_to_listen)
        print(f"\nListening to channels: {', '.join(channels_to_listen)}...Type '^c' to stop listening.") 

        try:
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    channel = message['channel'].decode('utf-8')
                    message_data = json.loads(message['data'])
                    sender = message_data.get('from')
                    msg = message_data.get('message')
                    print(f'[{channel}] {sender}: {msg}')
        except KeyboardInterrupt:
            print("\nStopped listening to channels.")
            for channel in channels_to_listen:
                self.pubsub.unsubscribe(channel)


    def direct_message(self):
        """Send a dm to someone"""
        user_name = input("\nWho do you want to dm? ")
        message = input("\nEnter your message here: ")
        message_obj = {
            "from": self.username, 
            "message": message 
        }
        self.client.publish(user_name, json.dumps(message_obj)) 
        print(f"\nMessage sent to {user_name}!")

    def list_channels(self):
        """List all available channels"""
        print("\nActive channels: ", self.client.pubsub_channels())

    def weather(self):
        """Get the weather forecast for your city"""
        city = input("\nChoose a city to get the weather forecast for: ")
        cmd = f"curl wttr.in/{city}"
        os.system(cmd)

    def show_fact(self):
        """Get a random fact (it might be bird-related)"""
        path = "db.json" 
        with open(path, "r") as json_file:
            data = json.load(json_file)
            facts_data = data["random_facts"]
            # Randomly select a field from "random_facts"
            random_key = random.choice(list(facts_data.keys())) 
            # print random fact about groups of birds
            print(f"\nDid you know? {facts_data[random_key]}")

    def show_user_info(self):
        """Get info about a user"""
        user_name = input("\nWho do you want to retrieve data for? ")
        user_key = f"user:{user_name}"
        # Use hgetall to retrieve all field-value pairs for the user key
        user_details = self.client.hgetall(user_key)
        # Decode the values from bytes to strings (assuming they are stored as strings)
        user_details = {field.decode('utf-8'): value.decode('utf-8') for field, value in user_details.items()}
        print(user_details)

    def show_help(self):
        """List of commands."""
        print(self.opts_message)

    def quit_chat(self):
        """Exit the chat."""
        print("\nGoodbye!")
        exit()

    def run(self):
        print(self.intro_message)
        while True:
            print("\n")
            print(self.opts_message)
            choice = input("\nWhat would you like to do? ")
            action = self.commands.get(choice)
            if action:
                action()
            elif choice.startswith('!'):
                bot.get_docstring(choice[1:])
                continue
            else:
                print("\nI don't recognize that command. Let's start over.")

if __name__ == "__main__":
    bot = Chatbot(username="Cathy", host="localhost", port=6379)
    bot.run()
