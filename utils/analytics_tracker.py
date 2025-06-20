import time


class AnalyticsTracker:
    def __init__(self, redis_client, bot_name):
        self.client = redis_client
        self.bot_name = bot_name

    def track_generation(self, channel):
        key = f"analytics:{self.bot_name}:{channel}:generations"
        self.client.incr(key)

    def track_turn(self, channel):
        key = f"analytics:{self.bot_name}:{channel}:turns"
        self.client.incr(key)

    def track_message_received(self, channel):
        key = f"analytics:{self.bot_name}:{channel}:received"
        self.client.incr(key)

    def track_message_ignored(self, channel):
        key = f"analytics:{self.bot_name}:{channel}:ignored"
        self.client.incr(key)

    def track_processing_time(self, channel, duration):
        key = f"analytics:{self.bot_name}:{channel}:processing_time"
        self.client.rpush(key, duration)
