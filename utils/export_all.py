import redis
import csv
import json
import datetime
import os
import sys

# Insert the root directory into the sys.path
sys.path.insert(1, os.getcwd())
from config_loader import ConfigLoader
from config import AppConfig


def export_channel_history(client, channels, output_file):
    print(f"Exporting chat history to {output_file}...")

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["channel", "sender", "message"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for channel in channels:
            history_key = f"history:{channel}"
            messages = client.lrange(history_key, 0, -1)

            for raw_message in messages:
                payload = json.loads(raw_message)
                writer.writerow(
                    {
                        "channel": channel,
                        "sender": payload.get("from", ""),
                        "message": payload.get("message", ""),
                    }
                )

    print("Chat history export complete.")


def export_analytics(client, output_file="analytics_export.csv"):
    print("Scanning analytics keys in Redis...")

    keys = client.keys("analytics:*")
    metrics = {}

    for key in keys:
        parts = key.split(":")
        if len(parts) != 4:
            continue

        _, bot, channel, metric = parts
        bot_key = f"{bot}:{channel}"

        if bot_key not in metrics:
            metrics[bot_key] = {}

        if metric == "processing_time":
            durations = [float(x) for x in client.lrange(key, 0, -1)]
            metrics[bot_key][metric] = durations
        else:
            count = int(client.get(key))
            metrics[bot_key][metric] = count

    print(f"Exporting analytics to {output_file}...")

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = [
            "Bot",
            "Channel",
            "Generations",
            "Turns",
            "MessagesReceived",
            "MessagesIgnored",
            "AvgProcessingTime",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for bot_key, data in metrics.items():
            bot, channel = bot_key.split(":")

            avg_time = (
                sum(data.get("processing_time", []))
                / len(data.get("processing_time", []))
                if data.get("processing_time")
                else 0.0
            )

            writer.writerow(
                {
                    "Bot": bot,
                    "Channel": channel,
                    "Generations": data.get("generations", 0),
                    "Turns": data.get("turns", 0),
                    "MessagesReceived": data.get("received", 0),
                    "MessagesIgnored": data.get("ignored", 0),
                    "AvgProcessingTime": round(avg_time, 3),
                }
            )

    print("Analytics export complete.")


if __name__ == "__main__":
    # Load config
    config_data = ConfigLoader.load_from_env()
    config = AppConfig(config_data)

    client = redis.StrictRedis(
        host=config.redis_host, port=config.redis_port, decode_responses=True
    )

    # Collect channels
    channels = client.smembers("channels")
    channels = [ch.decode() if isinstance(ch, bytes) else ch for ch in channels]

    # Create timestamped filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    chat_output = f"chat_export_{timestamp}.csv"
    analytics_output = f"analytics_export_{timestamp}.csv"

    export_channel_history(client, channels, chat_output)
    export_analytics(client, analytics_output)

    print("Export complete!")
