#!/usr/bin/env python3
"""
Emergence Explorer for Victor-0

Tracks and analyzes emergent signals across long runs.
This module helps us observe and understand behaviors that arise from the interaction
of Identity, Memory, Validation, Fractal Harness, and Routing.
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class TickTelemetry:
    tick: int
    trust: float
    fractal_variance: float
    action: str
    memory_count: int
    coherence_score: float = 0.0
    reflection: str = ""


class EmergenceExplorer:
    def __init__(self, log_path: str = "victor_zero_emergence.jsonl"):
        self.log_path = Path(log_path)
        self.history: List[TickTelemetry] = []
        self.trust_trend: List[float] = []
        self.variance_trend: List[float] = []
        self.action_counts: Dict[str, int] = defaultdict(int)
        self.reflection_keywords: Dict[str, int] = defaultdict(int)

    def record_tick(self, tick: int, trust: float, variance: float, action: str, memory_count: int, reflection: str = ""):
        coherence = self._calculate_coherence(trust, variance)

        telemetry = TickTelemetry(
            tick=tick,
            trust=trust,
            fractal_variance=variance,
            action=action,
            memory_count=memory_count,
            coherence_score=coherence,
            reflection=reflection
        )
        self.history.append(telemetry)
        self.trust_trend.append(trust)
        self.variance_trend.append(variance)
        self.action_counts[action] += 1

        # Simple reflection pattern detection
        for word in reflection.lower().split():
            if len(word) > 4:
                self.reflection_keywords[word] += 1

        self._log_to_file(telemetry)

    def _calculate_coherence(self, trust: float, variance: float) -> float:
        """Simple coherence score: high trust + low variance = high coherence"""
        return max(0.0, min(1.0, (trust * 0.7) + ((1.0 - min(variance, 1.0)) * 0.3)))

    def get_trust_trend(self) -> str:
        if not self.trust_trend:
            return "No data"
        avg = sum(self.trust_trend) / len(self.trust_trend)
        if len(self.trust_trend) > 5:
            recent = sum(self.trust_trend[-5:]) / 5
            if recent > avg + 0.05:
                return "Improving"
            elif recent < avg - 0.05:
                return "Declining"
        return "Stable"

    def get_top_reflection_patterns(self, top_n: int = 5) -> List[tuple]:
        return sorted(self.reflection_keywords.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_ticks": len(self.history),
            "avg_trust": sum(self.trust_trend) / len(self.trust_trend) if self.trust_trend else 0,
            "avg_variance": sum(self.variance_trend) / len(self.variance_trend) if self.variance_trend else 0,
            "trust_trend": self.get_trust_trend(),
            "top_actions": sorted(self.action_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "top_reflection_patterns": self.get_top_reflection_patterns()
        }

    def _log_to_file(self, telemetry: TickTelemetry):
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "tick": telemetry.tick,
                    "trust": telemetry.trust,
                    "variance": telemetry.fractal_variance,
                    "action": telemetry.action,
                    "coherence": telemetry.coherence_score,
                    "reflection": telemetry.reflection
                }) + "\n")
        except Exception:
            pass
