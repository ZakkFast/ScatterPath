from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship

from app.models.base import TimestampMixin, UUIDMixin
from app.models.enums import MilestoneStatus, PlanStatus, TaskStatus, WeekPlanStatus

if TYPE_CHECKING:
    from app.models.ai import AIProposal
    from app.models.goal import Goal


class Plan(UUIDMixin, TimestampMixin, table=True):
    __tablename__ = "plan"

    goal_id: UUID = Field(foreign_key="goal.id", index=True)
    summary: str
    status: PlanStatus = Field(default=PlanStatus.ACTIVE, index=True)

    goal: "Goal" = Relationship(back_populates="plans")
    milestones: list["Milestone"] = Relationship(back_populates="plan")
    week_plans: list["WeekPlan"] = Relationship(back_populates="plan")
    ai_proposals: list["AIProposal"] = Relationship(back_populates="plan")


class Milestone(UUIDMixin, TimestampMixin, table=True):
    __tablename__ = "milestone"

    plan_id: UUID = Field(foreign_key="plan.id", index=True)
    title: str
    description: str
    sort_order: int
    status: MilestoneStatus = Field(default=MilestoneStatus.PENDING, index=True)

    plan: Plan = Relationship(back_populates="milestones")
    tasks: list["Task"] = Relationship(back_populates="milestone")


class WeekPlan(UUIDMixin, TimestampMixin, table=True):
    __tablename__ = "week_plan"

    plan_id: UUID = Field(foreign_key="plan.id", index=True)
    week_number: int
    title: str
    focus: str
    starts_on: date
    ends_on: date
    status: WeekPlanStatus = Field(default=WeekPlanStatus.PENDING, index=True)

    plan: Plan = Relationship(back_populates="week_plans")
    tasks: list["Task"] = Relationship(back_populates="week_plan")


class Task(UUIDMixin, TimestampMixin, table=True):
    __tablename__ = "task"

    week_plan_id: UUID = Field(foreign_key="week_plan.id", index=True)
    milestone_id: UUID | None = Field(default=None, foreign_key="milestone.id", index=True)
    title: str
    description: str
    estimated_minutes: int
    why_it_matters: str
    success_criteria: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    sort_order: int
    completed_at: datetime | None = None
    skipped_at: datetime | None = None

    week_plan: WeekPlan = Relationship(back_populates="tasks")
    milestone: Milestone | None = Relationship(back_populates="tasks")
