import os
import yaml

class ConfigLoader:
    @staticmethod
    def load_from_env() -> dict:
        config_file = os.getenv("APP_CONFIG", "configs/app.yaml")
        with open(config_file, "r") as f:
            return yaml.safe_load(f)
