from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.ai import AIProposal, AIUsageLog
    from app.models.goal import Goal
    from app.models.parking_lot import ParkingLotItem


class UserProfile(UUIDMixin, TimestampMixin, table=True):
    __tablename__ = "user_profile"

    auth_provider_user_id: str = Field(index=True, unique=True)
    email: str = Field(index=True)
    display_name: str | None = None

    goals: list["Goal"] = Relationship(back_populates="user")
    parking_lot_items: list["ParkingLotItem"] = Relationship(back_populates="user")
    ai_proposals: list["AIProposal"] = Relationship(back_populates="user")
    ai_usage_logs: list["AIUsageLog"] = Relationship(back_populates="user")
