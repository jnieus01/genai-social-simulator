# Redis Chatbot

Cathy is an interactive command-line chatbot that leverages Redis for its backend operations. Users can perform a variety of tasks like joining channels, sending messages, listening to messages, retrieving random facts (possibly about birds), checking weather forecasts with wttr.in (created by @igor_chubin) and more.

## Features

- **User Identification:** Register yourself with name, age, and location.
- **Channel Operations:** Join, leave, send messages to, and listen to channels.
- **Direct Messaging:** Send direct messages to specific users.
- **Weather Forecast:** Get a weather forecast for a selected city using the wttr.in service as developed by @igor_chubin.
- **Random Facts:** Retrieve random facts.
- **Help:** List all available commands with their brief descriptions.

## Prerequisites

- Python 3

## How to Run

Download the project repo onto your local device. 

If you have docker installed, you may run the following to spin up the app's docker container: 

```bash
docker-compose up
```

To run the app, execute the following in your command line in the same working directory as the rest of the project repo: 

```bash
python redis_chat_app.py
```

4. Interact with Cathy using the displayed command options.

## Usage

After launching the chatbot, you'll be greeted with a list of command options. You can:

- Identify yourself with the `identify` command.
- Join chat channels with the `join` command.
- Send messages to channels with the `send` command.
- ... and more! Use the `!help` command for a complete list of available actions.

## Developer Notes

- The chatbot uses a sample `db.json` for random facts data.
- Data persistence and user messages are managed by Redis. Ensure your Redis server configurations are correct in the script (default is `host='redis', port=6379`).
- The chatbot uses the `pubsub` feature of Redis for channels and messaging.

### AI Usage
This code was developed while leveraging ChatGPT 3.5 and 4.0. Here's how I used ChatGPT to assist me in programming and debugging. Note: All code developed in conjunction with prompt engineering was reviewed and tested by me. 

1. **Docker and Redis Setup:**
   - I prepared a `docker-compose.yml` file for a Docker setup with Redis and a Python application to help id any syntax errors.

2. **Python Redis Chatroom:**
   - I shared an Python script that instantiated the initial version of the Chatbot class, its attributes and methods. 
   - I prompted ChatGPT 3.5 to generate code snippets for subscribing and publishing to a Redis channel and handling errors.

3. **Python Classes and Methods:**
   - I prompted ChatGPT 3.5 to provide high-level information about Python classes, class attributes, and methods in the context of object-oriented programming.

4. **JSON Data:**
   - I provided a simple .JSON file and prompted ChatGPT 3.5 to correct any syntax errors according to standard JSON format. 

5. **Debugging Assistance:**
   - I prompted ChatGPT 3.5 for assistance with debugging error messages related to Redis and Python code.

6. **Code Refactoring**
   - I provided ChatGPT 4.0 with my completed app and prompted it to refactor my script. 

## Contributions
Author: Jordan Nieusma
