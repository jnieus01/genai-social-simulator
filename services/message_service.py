import json

class MessageService:
    def __init__(self, redis_client, pubsub, username):
        self._client = redis_client
        self._pubsub = pubsub
        self._username = username

    def send_to_channel(self, channel, message):
        msg = {
            "from": self._username,
            "message": message
        }
        self._client.publish(channel, json.dumps(msg))

    def send_direct_message(self, recipient_username, message):
        msg = {
            "from": self._username,
            "message": message
        }
        self._client.publish(recipient_username, json.dumps(msg))

    def receive_direct_message(self, recipient_username, message):
        pass