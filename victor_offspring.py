#!/usr/bin/env python3
"""
Victor Offspring with Hierarchical Planning

Now includes:
- Hybrid Memory
- Active Goals
- Hierarchical Planning (Strategic → Tactical → Operational)
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    from planning.hierarchical_planner import HierarchicalPlanner, PlanLevel
except ImportError:
    HierarchicalPlanner = None
    PlanLevel = None


@dataclass
class Goal:
    description: str
    priority: float = 0.5
    progress: float = 0.0


class VictorOffspring:
    def __init__(self, name: str = "Victor-0"):
        self.name = name
        self.tick = 0
        self.kill_switch = False
        self.goals: List[Goal] = []
        self.planner = HierarchicalPlanner() if HierarchicalPlanner else None
        self.current_plan = None

    def add_goal(self, description: str, priority: float = 0.6):
        goal = Goal(description=description, priority=priority)
        self.goals.append(goal)

        if self.planner:
            plan = self.planner.decompose_goal(description)
            self.current_plan = plan
            print(f"[Planning] Created hierarchical plan for: {description}")

    def step(self):
        if self.kill_switch:
            return {"status": "halted"}

        self.tick += 1

        if self.goals:
            top_goal = max(self.goals, key=lambda g: g.priority)
            action = f"work_on: {top_goal.description}"
        else:
            action = "explore"

        # Simple progress on goals
        for goal in self.goals:
            goal.progress = min(1.0, goal.progress + 0.05)

        return {
            "tick": self.tick,
            "action": action,
            "active_goals": len(self.goals)
        }

    def run(self, ticks: int = 30):
        print(f"[Victor Offspring] Running with Hierarchical Planning for {ticks} ticks...")
        for _ in range(ticks):
            if self.kill_switch:
                break
            result = self.step()
            print(f"Tick {result['tick']}: {result['action']}")
            time.sleep(0.05)

        if self.current_plan and self.planner:
            print("\n=== Current Plan Tree ===")
            print(self.planner.get_plan_tree(self.current_plan.id))


if __name__ == "__main__":
    v = VictorOffspring()
    v.add_goal("Achieve long-term coherence and persistent identity", priority=0.9)
    v.run(25)
