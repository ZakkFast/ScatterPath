"""create core tables

Revision ID: 202606160001
Revises:
Create Date: 2026-06-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "202606160001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_profile",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("auth_provider_user_id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_profile_auth_provider_user_id", "user_profile", ["auth_provider_user_id"], unique=True)
    op.create_index("ix_user_profile_email", "user_profile", ["email"], unique=False)

    op.create_table(
        "ai_usage_log",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("action_type", sa.String(length=14), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("used_hosted_key", sa.Boolean(), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("estimated_cost", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user_profile.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_usage_log_action_type", "ai_usage_log", ["action_type"], unique=False)
    op.create_index("ix_ai_usage_log_user_id", "ai_usage_log", ["user_id"], unique=False)

    op.create_table(
        "goal",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("timeframe", sa.String(), nullable=True),
        sa.Column("available_minutes_per_day", sa.Integer(), nullable=False),
        sa.Column("available_days_per_week", sa.Integer(), nullable=False),
        sa.Column("current_situation", sa.String(), nullable=False),
        sa.Column("constraints", sa.String(), nullable=True),
        sa.Column("status", sa.String(length=9), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user_profile.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_goal_status", "goal", ["status"], unique=False)
    op.create_index("ix_goal_user_id", "goal", ["user_id"], unique=False)

    op.create_table(
        "parking_lot_item",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("goal_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("reason_parked", sa.String(), nullable=True),
        sa.Column("source", sa.String(length=12), nullable=False),
        sa.Column("status", sa.String(length=9), nullable=False),
        sa.ForeignKeyConstraint(["goal_id"], ["goal.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user_profile.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_parking_lot_item_goal_id", "parking_lot_item", ["goal_id"], unique=False)
    op.create_index("ix_parking_lot_item_source", "parking_lot_item", ["source"], unique=False)
    op.create_index("ix_parking_lot_item_status", "parking_lot_item", ["status"], unique=False)
    op.create_index("ix_parking_lot_item_user_id", "parking_lot_item", ["user_id"], unique=False)

    op.create_table(
        "plan",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("goal_id", sa.Uuid(), nullable=False),
        sa.Column("summary", sa.String(), nullable=False),
        sa.Column("status", sa.String(length=8), nullable=False),
        sa.ForeignKeyConstraint(["goal_id"], ["goal.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_plan_goal_id", "plan", ["goal_id"], unique=False)
    op.create_index("ix_plan_status", "plan", ["status"], unique=False)

    op.create_table(
        "ai_proposal",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("goal_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=True),
        sa.Column("type", sa.String(length=14), nullable=False),
        sa.Column("summary", sa.String(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(length=9), nullable=False),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("discarded_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["goal_id"], ["goal.id"]),
        sa.ForeignKeyConstraint(["plan_id"], ["plan.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user_profile.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_proposal_goal_id", "ai_proposal", ["goal_id"], unique=False)
    op.create_index("ix_ai_proposal_plan_id", "ai_proposal", ["plan_id"], unique=False)
    op.create_index("ix_ai_proposal_status", "ai_proposal", ["status"], unique=False)
    op.create_index("ix_ai_proposal_type", "ai_proposal", ["type"], unique=False)
    op.create_index("ix_ai_proposal_user_id", "ai_proposal", ["user_id"], unique=False)

    op.create_table(
        "milestone",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=9), nullable=False),
        sa.ForeignKeyConstraint(["plan_id"], ["plan.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_milestone_plan_id", "milestone", ["plan_id"], unique=False)
    op.create_index("ix_milestone_status", "milestone", ["status"], unique=False)

    op.create_table(
        "week_plan",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("week_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("focus", sa.String(), nullable=False),
        sa.Column("starts_on", sa.Date(), nullable=False),
        sa.Column("ends_on", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=9), nullable=False),
        sa.ForeignKeyConstraint(["plan_id"], ["plan.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_week_plan_plan_id", "week_plan", ["plan_id"], unique=False)
    op.create_index("ix_week_plan_status", "week_plan", ["status"], unique=False)

    op.create_table(
        "task",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("week_plan_id", sa.Uuid(), nullable=False),
        sa.Column("milestone_id", sa.Uuid(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False),
        sa.Column("why_it_matters", sa.String(), nullable=False),
        sa.Column("success_criteria", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(length=9), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("skipped_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["milestone_id"], ["milestone.id"]),
        sa.ForeignKeyConstraint(["week_plan_id"], ["week_plan.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_task_milestone_id", "task", ["milestone_id"], unique=False)
    op.create_index("ix_task_status", "task", ["status"], unique=False)
    op.create_index("ix_task_week_plan_id", "task", ["week_plan_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_task_week_plan_id", table_name="task")
    op.drop_index("ix_task_status", table_name="task")
    op.drop_index("ix_task_milestone_id", table_name="task")
    op.drop_table("task")

    op.drop_index("ix_week_plan_status", table_name="week_plan")
    op.drop_index("ix_week_plan_plan_id", table_name="week_plan")
    op.drop_table("week_plan")

    op.drop_index("ix_milestone_status", table_name="milestone")
    op.drop_index("ix_milestone_plan_id", table_name="milestone")
    op.drop_table("milestone")

    op.drop_index("ix_ai_proposal_user_id", table_name="ai_proposal")
    op.drop_index("ix_ai_proposal_type", table_name="ai_proposal")
    op.drop_index("ix_ai_proposal_status", table_name="ai_proposal")
    op.drop_index("ix_ai_proposal_plan_id", table_name="ai_proposal")
    op.drop_index("ix_ai_proposal_goal_id", table_name="ai_proposal")
    op.drop_table("ai_proposal")

    op.drop_index("ix_plan_status", table_name="plan")
    op.drop_index("ix_plan_goal_id", table_name="plan")
    op.drop_table("plan")

    op.drop_index("ix_parking_lot_item_user_id", table_name="parking_lot_item")
    op.drop_index("ix_parking_lot_item_status", table_name="parking_lot_item")
    op.drop_index("ix_parking_lot_item_source", table_name="parking_lot_item")
    op.drop_index("ix_parking_lot_item_goal_id", table_name="parking_lot_item")
    op.drop_table("parking_lot_item")

    op.drop_index("ix_goal_user_id", table_name="goal")
    op.drop_index("ix_goal_status", table_name="goal")
    op.drop_table("goal")

    op.drop_index("ix_ai_usage_log_user_id", table_name="ai_usage_log")
    op.drop_index("ix_ai_usage_log_action_type", table_name="ai_usage_log")
    op.drop_table("ai_usage_log")

    op.drop_index("ix_user_profile_email", table_name="user_profile")
    op.drop_index("ix_user_profile_auth_provider_user_id", table_name="user_profile")
    op.drop_table("user_profile")
