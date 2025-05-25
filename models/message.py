from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
from typing import Any, Dict

@dataclass(slots=True, frozen=True)
class Message:
    sender: str
    body: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_json(self):
        return json.dumps({
            "from": self.sender,
            "message": self.body, 
            "timestamp": self.timestamp.isoformat()
        })

    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        data = json.loads(json_str)

        def _dat(key: str) -> str:
            # try string first, then bytes
            if key in data:
                v = data[key]
            elif key.encode() in data:
                v = data[key.encode()]
            else:
                raise ValueError(f"Missing '{key}' in message hash")
            return v.decode() if isinstance(v, (bytes, bytearray)) else v

        return cls(sender=data["from"], body=data["message"], timestamp=datetime.fromisoformat(data["timestamp"]))
