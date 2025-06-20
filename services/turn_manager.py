import random
import yaml
from models.prompt import Prompt
import os
import sys

sys.path.insert(1, os.getcwd())
from config_loader import ConfigLoader
from config import AppConfig


class TurnManager:
    def __init__(self, redis_client, bots, config_path: str = "configs/app.yaml"):
        self._client = redis_client
        self._bots = bots
        # Load configs
        config_data = ConfigLoader.load_from_env()
        config = AppConfig(config_data)

        self._prompts = {
            name: Prompt(prompt=prompt_text)
            for name, prompt_text in config.prompts.items()
        }

    def initialize_turn(self, channel, config_first_bot):
        key = f"turn:{channel}"

        if self._client.exists(key):
            return  # turn state already initialized

        if config_first_bot == "random":
            first_bot = random.choice(self._bots)
        else:
            first_bot = config_first_bot

        self._client.set(key, first_bot)

    def is_my_turn(self, channel, bot_name):
        key = f"turn:{channel}"
        current_turn = self._client.get(key)
        return current_turn == bot_name

    def advance_turn(self, channel, current_bot):
        key = f"turn:{channel}"
        next_bot = self._next_bot(current_bot)
        self._client.set(key, next_bot)

    def _next_bot(self, current_bot):
        idx = self._bots.index(current_bot)
        next_idx = (idx + 1) % len(self._bots)
        return self._bots[next_idx]

    def get_prompt(self, bot_name: str) -> Prompt:
        return self._prompts.get(bot_name, Prompt(prompt=""))
