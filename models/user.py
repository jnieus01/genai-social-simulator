from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from uuid import uuid4
from typing import Any, Dict

@dataclass(slots=True, frozen=True)
class User:
    name: str
    age: int
    location: str
    uid: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.name:
            raise ValueError("User.name cannot be empty")
        if int(self.age) < 0:
            raise ValueError("User.age cannot be negative")
        
    def to_redis_hash(self) -> Dict[str, str]:
        """Return a flat string→string dict suitable for HSET."""
        d = asdict(self)
        # Convert any non-string values
        d["age"] = str(d["age"])
        d["created_at"] = d["created_at"].isoformat()
        return {k: str(v) for k, v in d.items()}

    @classmethod
    def from_redis_hash(cls, data: Dict[str, Any]) -> "User":
        """Create from a hash that may contain bytes or str."""
        def _val(key: str) -> str:
            # try string first, then bytes
            if key in data:
                v = data[key]
            elif key.encode() in data:
                v = data[key.encode()]
            else:
                raise ValueError(f"Missing '{key}' in user hash")
            return v.decode() if isinstance(v, (bytes, bytearray)) else v

        return cls(
            name=_val("name"),
            age=int(_val("age")),
            location=_val("location"),
            uid=_val("uid"),
            created_at=datetime.fromisoformat(_val("created_at")),
        )
