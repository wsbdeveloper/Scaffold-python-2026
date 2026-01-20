"""Initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela de applicants
    op.create_table(
        'applicants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_number', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('monthly_income', sa.Float(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_applicants_document_number', 'applicants', ['document_number'], unique=True)

    # Criar tabela de proposals
    op.create_table(
        'proposals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('applicant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('requested_amount', sa.Float(), nullable=False),
        sa.Column('installments', sa.Integer(), nullable=False),
        sa.Column('product_type', sa.Enum('PERSONAL_LOAN', 'PAYROLL_LOAN', 'CREDIT_CARD', name='producttype'), nullable=False),
        sa.Column('channel', sa.Enum('APP', 'BACKOFFICE', 'PARTNER_X', name='channel'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['applicant_id'], ['applicants.id']),
    )

    # Criar tabela de policies
    op.create_table(
        'policies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('product_types', sa.JSON(), nullable=False),
        sa.Column('channels', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_policies_name', 'policies', ['name'])

    # Criar tabela de decisions
    op.create_table(
        'decisions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('proposal_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.Enum('APPROVED', 'REJECTED', 'PENDING_DOCS', name='decisionstatus'), nullable=False),
        sa.Column('policy_name', sa.String(), nullable=False),
        sa.Column('policy_version', sa.String(), nullable=False),
        sa.Column('rule_results', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['proposal_id'], ['proposals.id']),
    )
    op.create_index('ix_decisions_proposal_id', 'decisions', ['proposal_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_decisions_proposal_id', table_name='decisions')
    op.drop_table('decisions')
    op.drop_index('ix_policies_name', table_name='policies')
    op.drop_table('policies')
    op.drop_table('proposals')
    op.drop_index('ix_applicants_document_number', table_name='applicants')
    op.drop_table('applicants')
    op.execute('DROP TYPE IF EXISTS decisionstatus')
    op.execute('DROP TYPE IF EXISTS channel')
    op.execute('DROP TYPE IF EXISTS producttype')
