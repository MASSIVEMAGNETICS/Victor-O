import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

@dataclass
class MemoryEntry:
    id: str
    kind: str
    content: Any
    timestamp: str
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)

class LayeredMemory:
    def __init__(self, path: str = "memory.jsonl"):
        self.path = Path(path)
        self.working: List[MemoryEntry] = []

    def add(self, kind: str, content: Any, importance: float = 0.5):
        entry = MemoryEntry(str(uuid.uuid4()), kind, content, datetime.now(timezone.utc).isoformat(), importance)
        self.working.append(entry)
        if len(self.working) > 100:
            self.working.pop(0)

    def recent(self, n: int = 10):
        return self.working[-n:]