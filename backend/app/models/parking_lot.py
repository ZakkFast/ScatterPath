from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from app.models.base import TimestampMixin, UUIDMixin
from app.models.enums import ParkingLotItemSource, ParkingLotItemStatus

if TYPE_CHECKING:
    from app.models.goal import Goal
    from app.models.user import UserProfile


class ParkingLotItem(UUIDMixin, TimestampMixin, table=True):
    __tablename__ = "parking_lot_item"

    goal_id: UUID = Field(foreign_key="goal.id", index=True)
    user_id: UUID = Field(foreign_key="user_profile.id", index=True)
    title: str
    description: str | None = None
    reason_parked: str | None = None
    source: ParkingLotItemSource = Field(default=ParkingLotItemSource.MANUAL, index=True)
    status: ParkingLotItemStatus = Field(default=ParkingLotItemStatus.ACTIVE, index=True)

    goal: "Goal" = Relationship(back_populates="parking_lot_items")
    user: "UserProfile" = Relationship(back_populates="parking_lot_items")
