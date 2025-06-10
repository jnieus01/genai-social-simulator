import redis
import json
import yaml
import os
import sys
# Insert the root directory into the sys.path
sys.path.insert(1, os.getcwd())
from config_loader import ConfigLoader
from config import AppConfig


SEED_CONFIG_PATH = "configs/seed.yaml"

def load_seed_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    config_data = ConfigLoader.load_from_env()
    config = AppConfig(config_data)

    seed_config = load_seed_config(SEED_CONFIG_PATH)

    client = redis.StrictRedis(host=config.redis_host, port=config.redis_port, decode_responses=True)

    channel = seed_config.get("channel", config.default_channels[0])
    msg = seed_config["message"]
    seed_message = {
        "from": msg.get("from", "system"),
        "message": msg["body"]
    }

    client.publish(channel, json.dumps(seed_message))
    print(f"Seeded conversation in channel '{channel}' with message from '{seed_message['from']}'")