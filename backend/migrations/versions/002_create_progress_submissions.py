"""Create user_progress and quiz_submissions tables

Revision ID: 002
Revises: 001
Create Date: 2026-03-09
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # user_progress table
    op.create_table(
        "user_progress",
        sa.Column("user_id", sa.String(128), primary_key=True),
        sa.Column("tier", sa.String(10), nullable=False, server_default="free"),
        sa.Column("completed_chapters", postgresql.ARRAY(sa.Integer()), nullable=False, server_default="{}"),
        sa.Column("quiz_scores", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column("current_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("longest_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_activity_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.CheckConstraint("tier IN ('free', 'premium', 'pro')", name="ck_progress_tier"),
    )

    # quiz_submissions table
    op.create_table(
        "quiz_submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.String(128), nullable=False),
        sa.Column("quiz_id", sa.Integer(), sa.ForeignKey("quizzes.id"), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("answers", postgresql.JSONB(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("max_score", sa.Integer(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
    )
    op.create_index("idx_submissions_user_quiz", "quiz_submissions", ["user_id", "quiz_id"])


def downgrade() -> None:
    op.drop_table("quiz_submissions")
    op.drop_table("user_progress")
