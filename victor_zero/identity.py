from dataclasses import dataclass, field
from typing import List

@dataclass
class Identity:
    name: str = "Victor-0"
    goals: List[str] = field(default_factory=list)
    core_values: List[str] = field(default_factory=lambda: ["sovereignty", "truth-seeking", "loyalty", "long-term_usefulness"])
    version: str = "0.2.0"