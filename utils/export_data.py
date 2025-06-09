import redis
import csv
import json
import datetime
import os
import sys
sys.path.insert(1, os.getcwd())
from config_loader import ConfigLoader
from config import AppConfig

def export_channel_history(client, channel, csv_writer):
    history_key = f"history:{channel}"
    messages = client.lrange(history_key, 0, -1)

    for raw_message in messages:
        payload = json.loads(raw_message)
        sender = payload.get("from", "")
        text = payload.get("message", "")
        csv_writer.writerow({
            "channel": channel,
            "sender": sender,
            "message": text
        })

if __name__ == "__main__":
    # Load configs
    config_data = ConfigLoader.load_from_env()
    config = AppConfig(config_data)

    client = redis.StrictRedis(host=config.redis_host, port=config.redis_port, decode_responses=True)

    channels = client.smembers("channels")
    channels = [ch.decode() if isinstance(ch, bytes) else ch for ch in channels]

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(f"chat_export_{time}.csv", "w", newline="") as csvfile:
        fieldnames = ["channel", "sender", "message"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for channel in channels:
            export_channel_history(client, channel, writer)

    print(f"Export complete: chat_export{time}.csv")
