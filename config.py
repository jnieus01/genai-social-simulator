class AppConfig:
    def __init__(self, data):
        self.redis_host = data.get("redis", {}).get("host", "redis")
        self.redis_port = data.get("redis", {}).get("port", 6379)
        self.default_channels = data.get("channels", {}).get("defaults", ["general"])
        self.ollama_base_url = data.get("ollama", {}).get("base_url")
        self.bots = data.get("ollama", {}).get("bots", {})
        self.channel_turns = {
            ch: cfg.get("initial_bot", "random")
            for ch, cfg in data.get("channel_turns", {}).items()
        }
        self.prompt_prefix = data.get("cli", {}).get("prompt_prefix", "\n> ") # TODO 