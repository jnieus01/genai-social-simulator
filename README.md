# Redis Chat CLI

🚧 **UNDER DEVELOPMENT** 🚧  

This project is in an early, experimental state.  

By cloning or running this code, **you assume all risk**:  
- **No guarantee** of stability, security, or data integrity
- **APIs, commands, configuration, and file formats** may change without notice
- **No warranty**—use at your own discretion, and please back up any data before testing  

Just be aware that things may break!

## Features

- **User Registration:** Register your user.
- **Channel Operations:** Join, leave, send messages to, and listen to channels.
- **Direct Messaging:** Send direct messages to specific users.
- **Help:** List all available commands with their brief descriptions.

## Prerequisites

- Python 3
- Docker Desktop

## How to Run

Download the project repo onto your local device. 

If you have docker installed, you may run the following to spin up the app's docker container and then enter the running container:

```bash
docker compose up --build -d            # spin up container
docker exec -it chatbot-python bash     # enter app container
```

To run the app, execute the following in the chatbot-python container's command line: 

```bash
python -m chat.cli_adapter
```

4. Interact on the app

## Usage

After launching the chatbot, you'll be greeted with a list of command options. You can:

- Identify yourself with `self_identify`; you'll be prompted for your name, age, and location.
- Join chat channels with `join`; provide channel name(s) when prompted.
- Send messages to channels with `say`; provide the target channel, your name and a message to send.
- ... and more! Use the `!help` command for a complete list of available actions.

## Developer Notes
- Data persistence and user messages are managed by Redis. Ensure your Redis server configurations are correct in the config file.
  
### Features Under Development
- Receive weather forecast updates via wttr.in API (created by @igor_chubin)

### AI Usage
This code was developed while leveraging ChatGPT to assist with refactoring and debugging. All code developed was reviewed and tested by me. 

## Contributions
Author: Jordan Nieusma
