import json

class ChannelManager:
    def __init__(self, redis_client, username, default_channels):
        self._client = redis_client
        self._username = username
        self._channels_key = f"channels:{username}"
        self._default_channels = default_channels
        self._pubsub = self._client.pubsub()
        self._initialize_channels()

    def _initialize_channels(self):
        initialized_key = "channels:initialized"
        first_run = self._client.setnx(initialized_key, "1")
        if first_run:
            for ch in self._default_channels:
                self._client.sadd("channels", ch)
        else:
            existing = self._client.smembers("channels")
            decoded_existing = {ch.decode() if isinstance(ch, bytes) else ch for ch in existing}
            for ch in self._default_channels:
                if ch not in decoded_existing:
                    self._client.sadd("channels", ch)
        for ch in self._default_channels:
            self._client.sadd(self._channels_key, ch)
            self._pubsub.subscribe(ch)

    def subscribe_to(self, channels):
        for ch in channels:
            self._client.sadd("channels", ch)
            self._client.sadd(self._channels_key, ch)
            self._pubsub.subscribe(ch)

    def listen(self):
        return self._pubsub.listen()

    def publish(self, channel, message):
        self._client.publish(channel, message)
        self._client.rpush(f"history:{channel}", message)
    
    def unsubscribe_from(self, channel):
        self._client.srem(self._channels_key, channel)
        self._pubsub.unsubscribe(channel)

    def get_user_channels(self):
        members = self._client.smembers(self._channels_key)
        return [m.decode() if isinstance(m, bytes) else m for m in members]

    def get_all_channels(self):
        members = self._client.smembers("channels")
        return [m.decode() if isinstance(m, bytes) else m for m in members]