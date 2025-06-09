import redis
import json
import time
import os
import sys
# Insert the root directory into the sys.path
sys.path.insert(1, os.getcwd())
from config_loader import ConfigLoader
from config import AppConfig
from utils.colors import colorize

def observe():
    config_data = ConfigLoader.load_from_env()
    config = AppConfig(config_data)

    client = redis.StrictRedis(
        host=config.redis_host,
        port=config.redis_port,
        decode_responses=True
    )

    channel = config.default_channels[0]

    pubsub = client.pubsub()
    pubsub.subscribe(channel)

    print(colorize('system', f"🔎 Listening to channel '{channel}'...\n"))

    try:
        for message in pubsub.listen():
            if message.get("type") != "message":
                continue

            payload = json.loads(message["data"])
            sender = payload.get("from", "unknown")
            text = payload.get("message", "")

            print(colorize(sender, f"[{channel}] [{sender}]: {text}"))

    except KeyboardInterrupt:
        print(colorize('system', "\nObserver stopped."))

if __name__ == "__main__":
    observe()
