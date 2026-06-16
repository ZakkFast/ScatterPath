from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from app.models.base import TimestampMixin, UUIDMixin
from app.models.enums import GoalStatus

if TYPE_CHECKING:
    from app.models.ai import AIProposal
    from app.models.parking_lot import ParkingLotItem
    from app.models.plan import Plan
    from app.models.user import UserProfile


class Goal(UUIDMixin, TimestampMixin, table=True):
    __tablename__ = "goal"

    user_id: UUID = Field(foreign_key="user_profile.id", index=True)
    title: str
    description: str
    target_date: date | None = None
    timeframe: str | None = None
    available_minutes_per_day: int
    available_days_per_week: int
    current_situation: str
    constraints: str | None = None
    status: GoalStatus = Field(default=GoalStatus.ACTIVE, index=True)

    user: "UserProfile" = Relationship(back_populates="goals")
    plans: list["Plan"] = Relationship(back_populates="goal")
    parking_lot_items: list["ParkingLotItem"] = Relationship(back_populates="goal")
    ai_proposals: list["AIProposal"] = Relationship(back_populates="goal")
