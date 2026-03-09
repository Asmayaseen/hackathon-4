"""Create chapters, quizzes, quiz_questions, content_sections tables

Revision ID: 001
Revises:
Create Date: 2026-03-09
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # chapters table
    op.create_table(
        "chapters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("r2_key", sa.String(512), nullable=False, unique=True),
        sa.Column("order_index", sa.Integer(), nullable=False, unique=True),
        sa.Column("tier", sa.String(10), nullable=False, server_default="free"),
        sa.Column("quiz_id", sa.Integer(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("tier IN ('free', 'premium')", name="ck_chapter_tier"),
    )

    # quizzes table
    op.create_table(
        "quizzes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("chapter_id", sa.Integer(), sa.ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Add FK from chapters.quiz_id -> quizzes.id
    op.create_foreign_key("fk_chapters_quiz_id", "chapters", "quizzes", ["quiz_id"], ["id"], ondelete="SET NULL")

    # quiz_questions table
    op.create_table(
        "quiz_questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("quiz_id", sa.Integer(), sa.ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("options", postgresql.JSONB(), nullable=False),
        sa.Column("correct_option", sa.String(1), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("correct_option IN ('A','B','C','D')", name="ck_question_correct_option"),
    )
    op.create_index("idx_quiz_questions_quiz", "quiz_questions", ["quiz_id"])

    # content_sections table with tsvector for full-text search
    op.create_table(
        "content_sections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("chapter_id", sa.Integer(), sa.ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section_index", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "text_tsv",
            postgresql.TSVECTOR(),
            sa.Computed("to_tsvector('english', text)", persisted=True),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_content_sections_chapter", "content_sections", ["chapter_id"])
    op.create_index(
        "idx_content_sections_tsv",
        "content_sections",
        ["text_tsv"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_table("content_sections")
    op.drop_table("quiz_questions")
    op.drop_constraint("fk_chapters_quiz_id", "chapters", type_="foreignkey")
    op.drop_table("quizzes")
    op.drop_table("chapters")
