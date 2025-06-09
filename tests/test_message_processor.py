import json
from services.message_processor import MessageProcessor

def test_parse_valid_json():
    raw = {"data": json.dumps({"from": "Alice", "message": "Hello"})}
    result = MessageProcessor.parse(raw)
    assert result["from"] == "Alice"
    assert result["message"] == "Hello"

def test_parse_invalid_json():
    raw = {"data": "just a plain string"}
    result = MessageProcessor.parse(raw)
    assert result["from"] == "unknown"
    assert result["message"] == "just a plain string"
