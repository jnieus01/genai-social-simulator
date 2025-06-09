import json

class MessageProcessor:
    @staticmethod
    def parse(raw_message):
        try:
            payload = json.loads(raw_message["data"])
        except (ValueError, TypeError):
            payload = {"from": "unknown", "message": raw_message["data"]}
        return payload

    @staticmethod
    def build_message(sender, message):
        return json.dumps({"from": sender, "message": message})
