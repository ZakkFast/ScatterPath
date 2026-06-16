from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship

from app.models.base import TimestampMixin, UUIDMixin, utc_now
from app.models.enums import AIActionType, AIProposalStatus

if TYPE_CHECKING:
    from app.models.goal import Goal
    from app.models.plan import Plan
    from app.models.user import UserProfile


class AIProposal(UUIDMixin, TimestampMixin, table=True):
    __tablename__ = "ai_proposal"

    user_id: UUID = Field(foreign_key="user_profile.id", index=True)
    goal_id: UUID = Field(foreign_key="goal.id", index=True)
    plan_id: UUID | None = Field(default=None, foreign_key="plan.id", index=True)
    type: AIActionType = Field(index=True)
    summary: str
    payload: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    status: AIProposalStatus = Field(default=AIProposalStatus.PENDING, index=True)
    applied_at: datetime | None = None
    discarded_at: datetime | None = None

    user: "UserProfile" = Relationship(back_populates="ai_proposals")
    goal: "Goal" = Relationship(back_populates="ai_proposals")
    plan: Optional["Plan"] = Relationship(back_populates="ai_proposals")


class AIUsageLog(UUIDMixin, table=True):
    __tablename__ = "ai_usage_log"

    user_id: UUID = Field(foreign_key="user_profile.id", index=True)
    action_type: AIActionType = Field(index=True)
    provider: str
    used_hosted_key: bool
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost: float | None = None
    created_at: datetime = Field(default_factory=utc_now)

    user: "UserProfile" = Relationship(back_populates="ai_usage_logs")
