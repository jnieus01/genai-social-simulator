import time
import redis
import json
from config_loader import ConfigLoader
from config import AppConfig
from services.turn_manager import TurnManager
from services.channel_manager import ChannelManager
from services.bot_service import BotService
from services.ai_clients.ollama_client import OllamaClient

# Load configs
config_data = ConfigLoader.load_from_env()
config = AppConfig(config_data)

# Init Redis client shared across bots
client = redis.StrictRedis(
    host=config.redis_host,
    port=config.redis_port,
    decode_responses=True
)

# Init turn manager shared across bots
bots = list(config.bots.keys())
turn_manager = TurnManager(client, bots)

# Create bots and start them
def create_bot_service(username):
    bot_cfg = config.bots[username]
    channel_manager = ChannelManager(client, username, config.default_channels)
    ai_client = OllamaClient(config.ollama_base_url, bot_cfg["model"], bot_cfg["generation_config"])
    return BotService(username, channel_manager, ai_client, turn_manager, config.channel_turns)

if __name__ == "__main__":
    for username in bots:
        bot = create_bot_service(username)
        bot.start_in_background()
        print(f"{username} started.")

    while True:
        time.sleep(60)
