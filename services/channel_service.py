import json
import config

class ChannelService:
    DEFAULT_CHANNELS = config.DEFAULT_CHANNELS

    def __init__(self, redis_client, pubsub, username):
        self._client = redis_client
        self._pubsub = pubsub
        self._username = username
        self._ensure_default_channels()

    def _ensure_default_channels(self):
        """Ensure default channels exist in Redis."""
        if self._client.setnx("channels:initialized", "1"):
            for ch in self.DEFAULT_CHANNELS:
                self._client.sadd("channels", ch)

    def join_channels(self, channels):
        channels_key = f"channels:{self._username}"
        for channel in channels:
            self._client.sadd(channels_key, channel)
            self._pubsub.subscribe(channel)
        return self.get_user_channels()
    
    def listen(self, channel=None):
        """Listen for messages on subscribed channels."""
        if not channel:
            print("Please specify a channel to listen to.")
            return
        else:
            channel = channel.strip()

        self._pubsub.subscribe(channel)
        print(f"Listening to channel: {channel}... Type control-c to stop.")        
        try:
            for message in self._pubsub.listen():
                if message['type'] != 'message':
                    continue
                
                if message['type'] == 'message':
                    channel = message['channel']
                    message_data = json.loads(message['data'])
                    sender = message_data.get('from')
                    msg = message_data.get('message')
                    
                    print(f'[{channel}] {sender}: {msg}')
        
        except KeyboardInterrupt:
            print("\nStopped listening.")
            self._pubsub.unsubscribe(channel)

    def leave_channel(self, channel):
        channels_key = f"channels:{self._username}"
        self._client.srem(channels_key, channel)
        self._pubsub.unsubscribe(channel)

    def get_user_channels(self):
        channels_key = f"channels:{self._username}"
        channels = self._client.smembers(channels_key)
        return [ch for ch in channels]

    def list_all_channels(self):
        return [ch.decode() for ch in self._client.pubsub_channels()]
