import threading
import time
import json
import queue
from utils import get_logger, AnalyticsTracker

class BotService:
    def __init__(self, username, channel_manager, ai_client, turn_manager, turn_config):
        self._username = username
        self._channels = channel_manager
        self._ai = ai_client
        self._turn_manager = turn_manager
        self._turn_config = turn_config
        self._message_queue = queue.Queue()
        self._analytics = AnalyticsTracker(self._channels._client, self._username)
        self._log = get_logger(self._username)

    def start_in_background(self):
        threading.Thread(target=self.listen_and_enqueue, name=f"{self._username}-ListenerThread", daemon=True).start()
        threading.Thread(target=self.process_messages, name=f"{self._username}-ProcessorThread", daemon=True).start()
        time.sleep(0.05)

    def listen_and_enqueue(self):
        for message in self._channels.listen():
            if message.get("type") == "message":
                raw_channel = message.get("channel")
                channel = raw_channel.decode() if isinstance(raw_channel, bytes) else raw_channel

                self._log.info(f"Received message on channel '{channel}'")
                self._analytics.track_message_received(channel)

                self._message_queue.put(message)
                self._log.debug(f"Queue size: {self._message_queue.qsize()}")

    def process_messages(self):
        while True:
            message = self._message_queue.get()
            if self._message_queue.empty():
                time.sleep(0.1)

            raw_channel = message.get("channel")
            if raw_channel is None:
                continue

            channel = raw_channel.decode() if isinstance(raw_channel, bytes) else raw_channel
            payload = json.loads(message["data"])
            sender, text = payload.get("from", ""), payload.get("message", "")
            self._log.info(f"Processing message from '{sender}'")

            if sender == self._username:
                self._log.debug(f"Ignoring own message from '{self._username}'")
                self._analytics.track_message_ignored(channel)
                continue

            if channel not in self._turn_config:
                self._log.warning(f"Channel '{channel}' not configured for turns.")
                continue

            self._turn_manager.initialize_turn(channel, self._turn_config[channel])
            self._log.info(f"Initialized turn for channel '{channel}' with first bot: {self._turn_config[channel]}")

            if not self._turn_manager.is_my_turn(channel, self._username):
                self._log.info(f"Not {self._username}'s turn on channel '{channel}'")
                continue

            prompt = f"{sender} said: {text}"
            self._log.info("Generating response...")

            start = time.time()
            reply = self._ai.generate_response(prompt)
            duration = time.time() - start
            self._analytics.track_processing_time(channel, duration)
            self._analytics.track_generation(channel)
            self._analytics.track_turn(channel)

            if reply:
                response_msg = json.dumps({"from": self._username, "message": reply})
                self._channels.publish(channel, response_msg)
                self._log.info("Reply generated and published.")

                self._turn_manager.advance_turn(channel, self._username)
                self._log.info(f"Turn advanced for channel '{channel}' to {self._turn_manager._next_bot(self._username)}")