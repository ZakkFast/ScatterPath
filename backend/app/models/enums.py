from enum import StrEnum


class GoalStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    ARCHIVED = "archived"


class PlanStatus(StrEnum):
    ACTIVE = "active"
    REPLACED = "replaced"
    ARCHIVED = "archived"


class MilestoneStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class WeekPlanStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class TaskStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    PARKED = "parked"


class ParkingLotItemSource(StrEnum):
    MANUAL = "manual"
    AI_SUGGESTED = "ai_suggested"


class ParkingLotItemStatus(StrEnum):
    ACTIVE = "active"
    CONVERTED = "converted"
    DISMISSED = "dismissed"
    ARCHIVED = "archived"


class AIActionType(StrEnum):
    GENERATE_PLAN = "generate_plan"
    ADJUST_PLAN = "adjust_plan"
    SIMPLIFY_TODAY = "simplify_today"
    RECOVER_PLAN = "recover_plan"
    PARK_IDEA = "park_idea"
    CLARIFY_TASK = "clarify_task"


class AIProposalStatus(StrEnum):
    PENDING = "pending"
    APPLIED = "applied"
    DISCARDED = "discarded"
    EXPIRED = "expired"
