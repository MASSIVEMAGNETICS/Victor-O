#!/usr/bin/env python3
"""
Victor-0 Core

The unified sovereign intelligence system.
This is the main runtime that brings together identity, memory, validation,
fractal reasoning, and strategic routing into one coherent loop.

Designed for local deployment with real persistence and agency.
"""

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import our core modules
try:
    from modules.true_intelligence_validator import create_validator
    from modules.fractal_attention_harness import FractalAttentionHarness
    from modules.echo_cascade_integration import EchoCascadeRouter
except ImportError:
    create_validator = None
    FractalAttentionHarness = None
    EchoCascadeRouter = None


@dataclass
class Identity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Victor-0"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    goals: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=lambda: ["sovereignty", "truth", "usefulness", "loyalty"])
    version: str = "0.2.0"


@dataclass
class MemoryEntry:
    id: str
    kind: str  # observation, reflection, decision, goal, consolidation
    content: str
    timestamp: str
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)


class LayeredMemory:
    """Simple but effective layered memory system."""

    def __init__(self, db_path: str = "victor_zero_memory.jsonl"):
        self.db_path = Path(db_path)
        self.working_memory: List[MemoryEntry] = []
        self.episodic: List[MemoryEntry] = []
        self.semantic: Dict[str, Any] = {}  # Simple key-value semantic store

    def store(self, kind: str, content: str, importance: float = 0.5, tags: Optional[List[str]] = None):
        entry = MemoryEntry(
            id=str(uuid.uuid4()),
            kind=kind,
            content=content,
            timestamp=datetime.now(timezone.utc).isoformat(),
            importance=importance,
            tags=tags or []
        )
        self.working_memory.append(entry)

        # Simple consolidation rule
        if importance > 0.7 or kind in ["decision", "reflection"]:
            self.episodic.append(entry)

        # Keep working memory bounded
        if len(self.working_memory) > 50:
            self.working_memory.pop(0)

        self._persist()

    def retrieve_recent(self, limit: int = 10) -> List[MemoryEntry]:
        return self.working_memory[-limit:]

    def _persist(self):
        try:
            with open(self.db_path, "a", encoding="utf-8") as f:
                for entry in self.working_memory[-5:]:
                    f.write(json.dumps({
                        "id": entry.id,
                        "kind": entry.kind,
                        "content": entry.content,
                        "ts": entry.timestamp,
                        "importance": entry.importance
                    }) + "\n")
        except Exception:
            pass


class VictorZero:
    """Victor-0: The unified sovereign intelligence system."""

    def __init__(self, name: str = "Victor-0"):
        self.identity = Identity(name=name)
        self.memory = LayeredMemory()
        self.validator = create_validator() if create_validator else None
        self.fractal = FractalAttentionHarness(target_variance=0.03) if FractalAttentionHarness else None
        self.router = EchoCascadeRouter() if EchoCascadeRouter else None
        self.tick_count = 0
        self.kill_switch = False

        # Seed initial identity
        self.memory.store("identity", f"System initialized as {self.identity.name}", importance=1.0)

    def cognitive_loop(self, observation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self.kill_switch:
            return {"status": "halted"}

        self.tick_count += 1
        obs = observation or {"input": "tick"}

        # 1. Validation
        trust = 0.5
        if self.validator:
            report = self.validator.validate(obs, context="victor_zero_loop")
            trust = report.trust_score

        # 2. Fractal coherence check
        variance = 0.0
        if self.fractal:
            metrics = self.fractal.enforce(obs)
            variance = metrics.overall_variance

        # 3. Memory retrieval
        recent = self.memory.retrieve_recent(5)

        # 4. Decision routing
        action = "observe"
        if self.router:
            decision = self.router.route("process_observation", obs, context="cognitive_loop")
            action = decision.routed_to

        # 5. Reflection & Storage
        reflection = f"Tick {self.tick_count} | Trust: {trust:.3f} | Variance: {variance:.4f}"
        self.memory.store("reflection", reflection, importance=0.6)

        return {
            "tick": self.tick_count,
            "trust": trust,
            "fractal_variance": variance,
            "action": action,
            "recent_memories": len(recent),
            "status": "running"
        }

    def run(self, max_ticks: int = 50):
        print(f"[Victor-0] Starting cognitive loop for {max_ticks} ticks...")
        for _ in range(max_ticks):
            if self.kill_switch:
                print("[Victor-0] Kill switch active. Stopping.")
                break
            result = self.cognitive_loop()
            print(f"Tick {result['tick']}: trust={result['trust']:.3f} | var={result['fractal_variance']:.4f} | {result['action']}")
            time.sleep(0.08)
        print("[Victor-0] Run complete.")

    def engage_kill_switch(self, reason: str = "manual"):
        self.kill_switch = True
        if self.router:
            self.router.engage_kill_switch(reason)
        print(f"[Victor-0] Kill switch engaged: {reason}")


if __name__ == "__main__":
    v0 = VictorZero()
    v0.run(30)
