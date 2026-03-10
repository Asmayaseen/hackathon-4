"""create hybrid_usage table for Phase 2 cost tracking

Revision ID: 004
Revises: 003
Create Date: 2026-03-09
"""
from alembic import op
import sqlalchemy as sa

revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'hybrid_usage',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('feature', sa.String(50), nullable=False),  # 'assess' or 'synthesize'
        sa.Column('chapter_ids', sa.Text(), nullable=True),   # JSON array
        sa.Column('tokens_input', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('tokens_output', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('cost_usd', sa.Numeric(10, 6), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('ix_hybrid_usage_user_id', 'hybrid_usage', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_hybrid_usage_user_id', 'hybrid_usage')
    op.drop_table('hybrid_usage')
