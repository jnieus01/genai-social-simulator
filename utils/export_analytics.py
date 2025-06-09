import redis
import csv
import os 
import sys
# Insert the root directory into the sys.path
sys.path.insert(1, os.getcwd())
from config_loader import ConfigLoader
from config import AppConfig

def export_analytics(output_file="analytics_export.csv"):
    config_data = ConfigLoader.load_from_env()
    config = AppConfig(config_data)

    client = redis.StrictRedis(
        host=config.redis_host,
        port=config.redis_port,
        decode_responses=True
    )

    print("Scanning analytics keys in Redis...")

    # Get all analytics keys
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
            # list of durations
            durations = client.lrange(key, 0, -1)
            durations = [float(x) for x in durations]
            metrics[bot_key][metric] = durations
        else:
            count = int(client.get(key))
            metrics[bot_key][metric] = count

    # Write CSV
    print(f"Exporting to {output_file}...")

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = [
            "Bot", "Channel", 
            "Generations", 
            "Turns", 
            "MessagesReceived", 
            "MessagesIgnored", 
            "AvgProcessingTime"
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for bot_key, data in metrics.items():
            bot, channel = bot_key.split(":")

            avg_time = (
                sum(data.get("processing_time", [])) / len(data.get("processing_time", []))
                if data.get("processing_time") else 0.0
            )

            writer.writerow({
                "Bot": bot,
                "Channel": channel,
                "Generations": data.get("generations", 0),
                "Turns": data.get("turns", 0),
                "MessagesReceived": data.get("received", 0),
                "MessagesIgnored": data.get("ignored", 0),
                "AvgProcessingTime": round(avg_time, 3),
            })

    print("Export complete!")

if __name__ == "__main__":
    export_analytics()
