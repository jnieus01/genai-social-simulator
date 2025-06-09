import redis
import json
import os
import sys
# Insert the root directory into the sys.path
sys.path.insert(1, os.getcwd())
from config_loader import ConfigLoader
from config import AppConfig

if __name__ == "__main__":
    config_data = ConfigLoader.load_from_env()
    config = AppConfig(config_data)

    client = redis.StrictRedis(host=config.redis_host, port=config.redis_port, decode_responses=True)

    channel = config.default_channels[0]

    seed_message = {
        "from": "system",
        "message": "Discuss the future of AI and its impact on society. Keep your messages concise and focused.",
    }

    client.publish(channel, json.dumps(seed_message))
    print(f"Seeded conversation in channel '{channel}'")
