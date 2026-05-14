#!/usr/bin/env python3
"""
Hierarchical Planner for Victor-0 / Victor Offspring

Implements multi-level planning:
- Strategic (high-level goals)
- Tactical (sub-goals / milestones)
- Operational (concrete actions / steps)

This allows the system to break down complex goals into manageable hierarchies.
"""

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class PlanLevel(Enum):
    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"


@dataclass
class Plan:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    goal: str
    level: PlanLevel
    sub_plans: List["Plan"] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    progress: float = 0.0
    parent_id: Optional[str] = None

    def add_sub_plan(self, sub_plan: "Plan"):
        sub_plan.parent_id = self.id
        self.sub_plans.append(sub_plan)

    def add_step(self, step: str):
        self.steps.append(step)


class HierarchicalPlanner:
    def __init__(self):
        self.plans: dict = {}  # id -> Plan

    def create_plan(self, goal: str, level: PlanLevel = PlanLevel.STRATEGIC) -> Plan:
        plan = Plan(goal=goal, level=level)
        self.plans[plan.id] = plan
        return plan

    def decompose_goal(self, goal: str, max_depth: int = 2) -> Plan:
        """
        Simple hierarchical decomposition.
        In a more advanced version, this would use LLM reasoning or learned decomposition.
        """
        root = self.create_plan(goal, PlanLevel.STRATEGIC)

        if max_depth > 0:
            # Tactical level
            tactical = Plan(
                goal=f"Break down: {goal}",
                level=PlanLevel.TACTICAL,
                parent_id=root.id
            )
            root.add_sub_plan(tactical)

            # Operational steps (simple example)
            operational = Plan(
                goal=f"Execute steps for: {goal}",
                level=PlanLevel.OPERATIONAL,
                parent_id=tactical.id
            )
            operational.add_step("Analyze current state")
            operational.add_step("Identify required resources")
            operational.add_step("Take first concrete action")
            tactical.add_sub_plan(operational)

        self.plans[root.id] = root
        return root

    def get_plan_tree(self, plan_id: str, indent: int = 0) -> str:
        if plan_id not in self.plans:
            return "Plan not found"

        plan = self.plans[plan_id]
        result = "  " * indent + f"[{plan.level.value}] {plan.goal} (progress: {plan.progress:.0%})\n"

        for sub in plan.sub_plans:
            result += self.get_plan_tree(sub.id, indent + 1)

        return result

    def update_progress(self, plan_id: str, progress: float):
        if plan_id in self.plans:
            self.plans[plan_id].progress = max(0.0, min(1.0, progress))
